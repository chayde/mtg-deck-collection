#!/usr/bin/env python3
"""
scripts/forge_pod_sim.py — Headless 4-Player Commander Pod Simulator & Telemetry Engine

Orchestrates automated 4-AI Commander pod matches using the local MTG Forge rules engine
and the custom Java telemetry bridge (scripts/ForgePodRunner.java).

Key Features:
  - Focuses deep hand, draw, and board-state diagnostics on Seat 1 (the Hero / Test Deck)
    while pitting it against a 3-deck Opponent Gauntlet (Seats 2, 3, and 4).
  - Grades every Hero opening hand (and rejected mulligan hand) using the exact Scryfall-backed
    Gold Keep / Silver Keep / Synergy Trap / Desperation Keep rubric from multiplayer_goldfish.py.
  - Tracks turn-by-turn card draws, land drops, spell casts, commander casts/recasts,
    engine readiness turns, stranded cards in hand, interaction fired/received, and win vectors.
  - Supports multi-process parallel execution (--workers) across CPU cores.
  - Generates <deck_dir>/forge_pod_report.html, <deck_dir>/FORGE_POD_LOG.md, and
    <deck_dir>/forge_pod_results.json.

Usage:
  python scripts/forge_pod_sim.py "commander_decks/Planning/ObekaSplitterOfSeconds" --games 8 --bracket 3
  python scripts/forge_pod_sim.py "UrDragonKibler" --pod "Karametra" "Sauron" "MerenReanimator" --games 12 --workers 4
"""

import argparse
import concurrent.futures
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import multiplayer_goldfish as gf
import sync_to_forge as stf

BRIDGE_JAVA = SCRIPTS_DIR / "ForgePodRunner.java"
BRIDGE_BUILD_DIR = REPO_ROOT / "cache" / "forge_bridge"

DEFAULT_GAUNTLETS: Dict[str, List[str]] = {
    "bracket2": [
        "YshtolaNightsBlessed",
        "Quantum Quandrix",
        "Frodo and Sam - Second Breakfast",
    ],
    "bracket3": [
        "Karametra",
        "Sauron",
        "MerenReanimator",
    ],
    "combat": [
        "UrDragon",
        "Karametra",
        "JinSakai",
    ],
}

FALLBACK_POOL = [
    "Karametra",
    "Sauron",
    "MerenReanimator",
    "UrDragon",
    "JinSakai",
    "Gisa The Hellraiser",
    "HearthhullTheWorldseed",
]


def find_forge_install() -> Tuple[Path, Path]:
    """Locates the Forge installation directory and highest-version desktop JAR."""
    candidates = [
        Path(os.environ.get("FORGE_INSTALL_DIR", "")) if os.environ.get("FORGE_INSTALL_DIR") else None,
        Path("C:/forge-mtg"),
        Path("C:/forge"),
        Path.home() / "forge-mtg",
        Path.home() / "AppData" / "Local" / "Forge",
    ]
    for c in candidates:
        if c and c.exists():
            jars = sorted(c.glob("forge-gui-desktop-*-jar-with-dependencies.jar"))
            if jars:
                return c, jars[-1]
    raise FileNotFoundError(
        "Could not locate MTG Forge installation or forge-gui-desktop-*-jar-with-dependencies.jar in C:/forge-mtg."
    )


def ensure_bridge_compiled(forge_jar: Path) -> Path:
    """Compiles scripts/ForgePodRunner.java against the Forge JAR if needed."""
    BRIDGE_BUILD_DIR.mkdir(parents=True, exist_ok=True)
    class_file = BRIDGE_BUILD_DIR / "ForgePodRunner.class"

    needs_compile = (
        not class_file.exists()
        or BRIDGE_JAVA.stat().st_mtime > class_file.stat().st_mtime
    )
    if needs_compile:
        javac = shutil.which("javac") or "javac"
        cmd = [
            javac,
            "-encoding",
            "UTF-8",
            "-cp",
            str(forge_jar),
            "-d",
            str(BRIDGE_BUILD_DIR),
            str(BRIDGE_JAVA),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to compile ForgePodRunner.java:\n{res.stderr}")
    return BRIDGE_BUILD_DIR


def resolve_deck_to_dck(identifier: str, forge_cmd_dir: Path) -> Tuple[str, Optional[Path]]:
    """
    Resolves a deck identifier (repo folder path, folder name, or Forge .dck name)
    to a synced .dck filename in forge_cmd_dir and its repo deck directory (if found).
    """
    p = Path(identifier)
    if not p.is_absolute():
        cand = REPO_ROOT / identifier
        if cand.exists():
            p = cand

    # Search repo commander_decks if identifier is a folder name like 'ObekaSplitterOfSeconds'
    if not p.exists():
        for sub in ("Owned", "Planning", "PreCons", "External"):
            cand = REPO_ROOT / "commander_decks" / sub / identifier
            if cand.exists():
                p = cand
                break
            # Also check reverse alias from KNOWN_FORGE_ALIASES
            for folder_name, alias in stf.KNOWN_FORGE_ALIASES.items():
                if alias.lower() == identifier.lower():
                    cand2 = REPO_ROOT / "commander_decks" / sub / folder_name
                    if cand2.exists():
                        p = cand2
                        break

    if p.exists():
        mox_path, md_path, deck_dir = stf.resolve_deck_files(p)
        if mox_path or md_path:
            ok, msg = stf.sync_deck_to_forge(deck_dir, forge_dir=forge_cmd_dir, dry_run=False)
            if ok:
                deck_name = stf.determine_forge_deck_name(deck_dir, forge_cmd_dir)
                return f"{deck_name}.dck", deck_dir

    # Otherwise check directly in forge_cmd_dir
    dck_name = identifier if identifier.endswith(".dck") else f"{identifier}.dck"
    direct = forge_cmd_dir / dck_name
    if direct.exists():
        # Try to find matching repo folder for metadata
        stem = direct.stem
        for sub in ("Owned", "Planning", "PreCons", "External"):
            base = REPO_ROOT / "commander_decks" / sub
            if not base.exists():
                continue
            for d in base.iterdir():
                if not d.is_dir():
                    continue
                if d.name.lower() == stem.lower() or stf.KNOWN_FORGE_ALIASES.get(d.name, "").lower() == stem.lower():
                    return direct.name, d
        return direct.name, None

    # Case-insensitive fallback in forge_cmd_dir
    for f in forge_cmd_dir.glob("*.dck"):
        if f.stem.lower() == identifier.lower().removesuffix(".dck"):
            return f.name, None

    raise FileNotFoundError(f"Could not resolve deck '{identifier}' in repository or {forge_cmd_dir}")


def load_hero_card_catalog(deck_dir: Optional[Path], dck_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Loads Scryfall card metadata and Goldfish classification (land, ramp, enabler, payoff, CMC, image)
    for all cards in the Hero deck.
    """
    gf._load_cache()
    card_names: List[str] = []

    if dck_path.exists():
        for line in dck_path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("[") or line.startswith("Name="):
                continue
            m = re.match(r"^\d+\s+([^|]+)", line)
            if m:
                card_names.append(m.group(1).strip())

    if deck_dir and (deck_dir / "moxfield_import.txt").exists():
        mox_file = deck_dir / "moxfield_import.txt"
        for line in mox_file.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("//") or line.endswith(":"):
                continue
            m = re.match(r"^\d+x?\s+(.+)$", line)
            if m:
                card_names.append(m.group(1).strip())

    catalog: Dict[str, Dict[str, Any]] = {}
    unique_names = sorted(set(card_names))

    for name in unique_names:
        sf = gf.get_scryfall(name)
        cd = gf.classify_card(name)
        img_uri = ""
        scryfall_uri = f"https://scryfall.com/search?q=!{ name.replace(' ', '+') }"
        type_line = ""
        mana_cost = ""
        if sf:
            scryfall_uri = sf.get("scryfall_uri") or scryfall_uri
            type_line = sf.get("type_line", "")
            mana_cost = sf.get("mana_cost", "")
            if "image_uris" in sf and sf["image_uris"].get("normal"):
                img_uri = sf["image_uris"]["normal"]
            elif "card_faces" in sf and sf["card_faces"]:
                face0 = sf["card_faces"][0]
                mana_cost = mana_cost or face0.get("mana_cost", "")
                if "image_uris" in face0 and face0["image_uris"].get("normal"):
                    img_uri = face0["image_uris"]["normal"]

        role_tags = []
        if cd.is_land:
            role_tags.append("Land")
        elif cd.is_mdfc_land:
            role_tags.append("MDFC Land")
        if cd.is_ramp or cd.is_mana_perm or cd.is_burst:
            role_tags.append("Ramp/Mana")
        if cd.is_enabler:
            role_tags.append("Enabler/Draw")
        if cd.is_payoff:
            role_tags.append("Payoff")
        if not role_tags:
            role_tags.append("Synergy/Plan")

        info = {
            "name": name,
            "cmc": cd.cmc,
            "mana_cost": mana_cost,
            "type_line": type_line,
            "is_land": cd.is_land,
            "is_mdfc_land": cd.is_mdfc_land,
            "is_ramp": cd.is_ramp or cd.is_mana_perm or cd.is_burst,
            "is_enabler": cd.is_enabler,
            "is_payoff": cd.is_payoff,
            "roles": role_tags,
            "image_uri": img_uri,
            "scryfall_uri": scryfall_uri,
        }
        catalog[name] = info
        catalog[name.lower()] = info
        # Also index front-face name for DFCs ("A // B" -> "A")
        if "//" in name:
            front = name.split("//")[0].strip()
            catalog[front] = info
            catalog[front.lower()] = info

    return catalog


def lookup_card_info(card_name: str, catalog: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Finds card classification info from the Hero catalog, falling back to Scryfall cache."""
    if card_name in catalog:
        return catalog[card_name]
    low = card_name.lower()
    if low in catalog:
        return catalog[low]
    if "//" in card_name:
        front = card_name.split("//")[0].strip().lower()
        if front in catalog:
            return catalog[front]
    # Check global scryfall cache without network delay if possible
    entry = gf._cache.get(low)
    if entry and entry.get("data"):
        sf = entry["data"]
        cd = gf.classify_card(card_name)
        img_uri = ""
        if "image_uris" in sf and sf["image_uris"].get("normal"):
            img_uri = sf["image_uris"]["normal"]
        elif "card_faces" in sf and sf["card_faces"] and "image_uris" in sf["card_faces"][0]:
            img_uri = sf["card_faces"][0]["image_uris"].get("normal", "")
        return {
            "name": card_name,
            "cmc": cd.cmc,
            "mana_cost": sf.get("mana_cost", ""),
            "type_line": sf.get("type_line", ""),
            "is_land": cd.is_land,
            "is_mdfc_land": cd.is_mdfc_land,
            "is_ramp": cd.is_ramp or cd.is_mana_perm or cd.is_burst,
            "is_enabler": cd.is_enabler,
            "is_payoff": cd.is_payoff,
            "roles": ["Card"],
            "image_uri": img_uri,
            "scryfall_uri": sf.get("scryfall_uri", f"https://scryfall.com/search?q=!{card_name.replace(' ', '+')}"),
        }
    return {
        "name": card_name,
        "cmc": 0,
        "mana_cost": "",
        "type_line": "",
        "is_land": any(b in card_name for b in ("Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes", "Tower", "Tomb", "Crypt", "Garden", "Fountain", "Shrine", "Pool", "Vents", "Grave", "Ground", "Foundry", "parlor", " verge", "land")),
        "is_mdfc_land": False,
        "is_ramp": False,
        "is_enabler": False,
        "is_payoff": False,
        "roles": ["Card"],
        "image_uri": "",
        "scryfall_uri": f"https://scryfall.com/search?q=!{card_name.replace(' ', '+')}",
    }


def grade_hand_quality(
    hand_cards: List[str],
    mulligans: int,
    catalog: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Applies the repository's exact Goldfish Opening Hand Quality rubric:
      - Gold Keep: 2-4 lands, >=1 ramp/mana, >=1 enabler
      - Synergy Trap: >=3 lands, 0 ramp/mana, 0 enablers, >=3 payoffs
      - Desperation Keep: mulliganed down to <=5 cards (and not Gold)
      - Silver Keep: 2-5 lands (playable keep without full Gold package)
      - Land Screw / Flood: <2 or >5 lands
    """
    infos = [lookup_card_info(c, catalog) for c in hand_cards]
    lands = sum(1 for x in infos if x["is_land"] or x["is_mdfc_land"])
    ramp = sum(1 for x in infos if x["is_ramp"] and not x["is_land"])
    enablers = sum(1 for x in infos if x["is_enabler"] and not x["is_land"])
    payoffs = sum(1 for x in infos if x["is_payoff"] and not x["is_land"])

    is_trap = (lands >= 3 and ramp == 0 and enablers == 0 and payoffs >= 3)
    if is_trap:
        grade = "Synergy Trap"
    elif 2 <= lands <= 4 and ramp >= 1 and enablers >= 1:
        grade = "Gold"
    elif mulligans > 0 and len(hand_cards) <= 5:
        grade = "Desperation"
    elif 2 <= lands <= 5:
        grade = "Silver"
    elif lands < 2:
        grade = "Mana Screw (<2 Lands)" if mulligans == 0 else "Desperation"
    else:
        grade = "Mana Flood (6+ Lands)" if mulligans == 0 else "Desperation"

    return {
        "grade": grade,
        "lands": lands,
        "ramp": ramp,
        "enablers": enablers,
        "payoffs": payoffs,
        "is_trap": is_trap,
        "hand_size": len(hand_cards),
    }


def run_worker_batch(
    worker_id: int,
    forge_dir: Path,
    forge_jar: Path,
    bridge_dir: Path,
    deck_dir: Path,
    dck_files: List[str],
    num_games: int,
    timeout_sec: int,
    ai_timeout_sec: int,
    base_seed: int,
    smart_mulligan: bool,
) -> List[Dict[str, Any]]:
    """Runs a batch of games inside one headless Forge JVM worker process."""
    sep = ";" if os.name == "nt" else ":"
    cp = f"{bridge_dir.resolve()}{sep}{forge_jar.resolve()}"
    java_bin = shutil.which("java") or "java"

    cmd = [
        java_bin,
        "-Xmx3072m",
        "-Dio.netty.tryReflectionSetAccessible=true",
        "-Dfile.encoding=UTF-8",
        "-cp",
        cp,
        "ForgePodRunner",
        "-D",
        str(deck_dir),
        "-d",
        *dck_files,
        "-n",
        str(num_games),
        "-c",
        str(timeout_sec),
        "-ai",
        str(ai_timeout_sec),
        "-s",
        str(base_seed),
        "-smartMulligan" if smart_mulligan else "-stockMulligan",
    ]

    proc_timeout = max(180, num_games * (timeout_sec + 25) + 60)
    r = subprocess.run(
        cmd,
        cwd=str(forge_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=proc_timeout,
    )

    games: List[Dict[str, Any]] = []
    for line in r.stdout.splitlines():
        if line.startswith("TELEMETRY_GAME_JSON:"):
            raw = line[len("TELEMETRY_GAME_JSON:") :].strip()
            try:
                games.append(json.loads(raw))
            except Exception as exc:
                print(f"[Worker {worker_id}] JSON parse warning: {exc}", file=sys.stderr)

    if not games and r.returncode != 0:
        raise RuntimeError(
            f"Worker {worker_id} failed (exit {r.returncode}):\nSTDOUT: {r.stdout[-500:]}\nSTDERR: {r.stderr[-500:]}"
        )
    return games


def enrich_and_aggregate(
    games: List[Dict[str, Any]],
    catalog: Dict[str, Dict[str, Any]],
    bracket: int,
    dck_files: List[str],
    wall_clock_sec: float,
) -> Dict[str, Any]:
    """Enriches per-game telemetry with Scryfall classifications and computes aggregate pod metrics."""
    target_turn = gf.BRACKET_TARGET_TURNS.get(bracket, 7)
    bracket_label = gf.BRACKET_NAMES.get(bracket, f"Bracket {bracket}")

    # Sort games deterministically by seed/index
    games.sort(key=lambda g: g.get("seed", 0))
    for idx, g in enumerate(games, start=1):
        g["game_index"] = idx

    hand_grades = Counter()
    rejected_grades = Counter()
    mulligan_counts = Counter()
    opening_hand_sizes: List[int] = []
    cmd_first_cast_turns: List[int] = []
    cmd_total_casts_per_game: List[int] = []
    engine_ready_turns: List[int] = []
    seat_wins = Counter()
    turn_order_wins = Counter()
    turn_order_games = Counter()
    win_reasons = Counter()

    # Turn-by-turn progression accumulators (Hero Turn 1..12)
    turn_accum: Dict[int, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))

    # Card-level performance counters for Seat 1
    card_in_kept_hand = Counter()
    card_in_winning_hand = Counter()
    card_drawn_count = Counter()
    card_cast_count = Counter()
    card_stranded_count = Counter()
    card_bottomed_count = Counter()

    opp_interaction_cards = Counter()
    hero_interaction_cards = Counter()

    for g in games:
        kept = g.get("hero_kept_hand", [])
        mulls = g.get("hero_mulligans", 0)
        mulligan_counts[mulls] += 1
        opening_hand_sizes.append(g.get("hero_opening_hand_size", len(kept)))

        kept_eval = grade_hand_quality(kept, mulls, catalog)
        g["hero_kept_hand_eval"] = kept_eval
        hand_grades[kept_eval["grade"]] += 1

        rej_evals = []
        for idx_m, m_hand in enumerate(g.get("hero_mulliganed_hands", [])):
            ev = grade_hand_quality(m_hand, idx_m, catalog)
            rej_evals.append({"hand": m_hand, "eval": ev})
            rejected_grades[ev["grade"]] += 1
        g["hero_mulliganed_evals"] = rej_evals

        for b_card in g.get("hero_bottomed_cards", []):
            card_bottomed_count[b_card] += 1

        hero_won = (g.get("winner_seat") == 1)
        for c in set(kept):
            card_in_kept_hand[c] += 1
            if hero_won:
                card_in_winning_hand[c] += 1

        for dr in g.get("hero_draws", []):
            card_drawn_count[dr["card"]] += 1

        # Classify spells cast by Hero & compute Engine Readiness Turn
        enablers_cast_by_turn: Dict[int, int] = defaultdict(int)
        draws_by_turn: Dict[int, int] = defaultdict(int)
        for dr in g.get("hero_draws", []):
            draws_by_turn[dr["hero_turn"]] += 1

        for sc in g.get("hero_spell_casts", []):
            c_name = sc["card"]
            card_cast_count[c_name] += 1
            c_info = lookup_card_info(c_name, catalog)
            sc["roles"] = c_info["roles"]
            sc["cmc"] = c_info["cmc"]
            if c_info["is_enabler"]:
                enablers_cast_by_turn[sc["hero_turn"]] += 1

        c_turns = g.get("hero_commander_cast_turns", [])
        if c_turns:
            cmd_first_cast_turns.append(c_turns[0])
        cmd_total_casts_per_game.append(len(c_turns))

        # Engine Readiness Turn: Commander cast <= T, (cumulative enablers >= 1 or cumulative extra draws >= 3), and mana_sources_ready >= 5
        cum_enablers = 0
        cum_draws = 0
        ready_turn: Optional[int] = None
        first_cmd_t = c_turns[0] if c_turns else None

        for snap in g.get("hero_turn_snapshots", []):
            ht = snap["hero_turn"]
            cum_enablers += enablers_cast_by_turn.get(ht, 0)
            cum_draws += draws_by_turn.get(ht, 0)
            cmd_deployed = (first_cmd_t is not None and first_cmd_t <= ht) or snap.get("commander_in_play", False)
            has_velocity = (cum_enablers >= 1 or cum_draws >= 3)
            if ready_turn is None and cmd_deployed and has_velocity and snap.get("mana_sources_ready", 0) >= 5:
                ready_turn = ht

            if ht <= 12:
                turn_accum[ht]["lands_total"].append(snap["lands_total"])
                turn_accum[ht]["mana_ready"].append(snap["mana_sources_ready"])
                turn_accum[ht]["creatures"].append(snap["creatures_count"])
                turn_accum[ht]["power"].append(snap["total_power"])
                turn_accum[ht]["hand_size"].append(snap["hand_size"])
                turn_accum[ht]["life"].append(snap["hero_life"])

        g["hero_engine_ready_turn"] = ready_turn
        if ready_turn is not None:
            engine_ready_turns.append(ready_turn)

        # Stranded cards in hand at end of Hero's last turn
        snaps = g.get("hero_turn_snapshots", [])
        if snaps:
            last_hand = snaps[-1].get("hand_cards", [])
            g["hero_final_hand"] = last_hand
            for c in set(last_hand):
                c_info = lookup_card_info(c, catalog)
                if not c_info["is_land"]:
                    card_stranded_count[c] += 1
        else:
            g["hero_final_hand"] = []

        # Interaction counters
        for ir in g.get("opp_interaction_vs_hero", []):
            opp_interaction_cards[ir["card"]] += 1
        for ir in g.get("hero_interaction_vs_opp", []):
            hero_interaction_cards[ir["card"]] += 1

        # Winner & Turn Order stats
        w_seat = g.get("winner_seat", 0)
        seat_wins[w_seat] += 1
        win_reasons[g.get("win_reason", "Unknown")] += 1

        hero_to = g.get("hero_turn_order_pos", 1)
        turn_order_games[hero_to] += 1
        if w_seat == 1:
            turn_order_wins[hero_to] += 1

    num_games = max(1, len(games))
    hero_deck_name = games[0].get("hero_deck", dck_files[0]) if games else dck_files[0]
    hero_commander = games[0].get("hero_commander", "Unknown") if games else "Unknown"

    # Seat summary table
    pod_seats_summary = []
    if games and games[0].get("seats"):
        for s_idx in range(len(games[0]["seats"])):
            seat_num = s_idx + 1
            s_deck = games[0]["seats"][s_idx]["deck"]
            s_cmd = games[0]["seats"][s_idx]["commander"]
            wins = seat_wins[seat_num]
            avg_spells = sum(g["seats"][s_idx]["spells_cast"] for g in games if len(g.get("seats", [])) > s_idx) / num_games
            avg_cmd_casts = sum(g["seats"][s_idx]["commander_casts"] for g in games if len(g.get("seats", [])) > s_idx) / num_games
            avg_peak_power = sum(g["seats"][s_idx]["peak_power_in_play"] for g in games if len(g.get("seats", [])) > s_idx) / num_games
            avg_mulls = sum(g["seats"][s_idx]["mulligans"] for g in games if len(g.get("seats", [])) > s_idx) / num_games
            pod_seats_summary.append({
                "seat": seat_num,
                "deck": s_deck,
                "commander": s_cmd,
                "wins": wins,
                "win_rate": round(100.0 * wins / num_games, 1),
                "avg_mulligans": round(avg_mulls, 2),
                "avg_commander_casts": round(avg_cmd_casts, 2),
                "avg_spells_cast": round(avg_spells, 1),
                "avg_peak_power": round(avg_peak_power, 1),
            })

    turn_progression = []
    for ht in sorted(turn_accum.keys()):
        d = turn_accum[ht]
        n_obs = len(d["lands_total"])
        if n_obs == 0:
            continue
        turn_progression.append({
            "hero_turn": ht,
            "games_alive": n_obs,
            "avg_lands": round(sum(d["lands_total"]) / n_obs, 2),
            "avg_mana_ready": round(sum(d["mana_ready"]) / n_obs, 2),
            "avg_creatures": round(sum(d["creatures"]) / n_obs, 2),
            "avg_power": round(sum(d["power"]) / n_obs, 1),
            "avg_hand_size": round(sum(d["hand_size"]) / n_obs, 2),
            "avg_life": round(sum(d["life"]) / n_obs, 1),
        })

    ready_on_time = sum(1 for t in engine_ready_turns if t <= target_turn)

    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "hero_deck": hero_deck_name,
        "hero_commander": hero_commander,
        "bracket": bracket,
        "bracket_label": bracket_label,
        "target_turn": target_turn,
        "num_games": len(games),
        "wall_clock_sec": round(wall_clock_sec, 2),
        "avg_game_duration_sec": round(sum(g.get("duration_ms", 0) for g in games) / (1000.0 * num_games), 2),
        "timeouts": sum(1 for g in games if g.get("timed_out")),
        "avg_hero_turns": round(sum(g.get("total_hero_turns", 0) for g in games) / num_games, 1),
        "avg_global_turns": round(sum(g.get("total_global_turns", 0) for g in games) / num_games, 1),
        "hero_wins": seat_wins[1],
        "hero_win_rate": round(100.0 * seat_wins[1] / num_games, 1),
        "pod_seats_summary": pod_seats_summary,
        "opening_hand_summary": {
            "avg_starting_hand_size": round(sum(opening_hand_sizes) / num_games, 2),
            "avg_mulligans": round(sum(g.get("hero_mulligans", 0) for g in games) / num_games, 2),
            "mulligan_distribution": {str(k): v for k, v in sorted(mulligan_counts.items())},
            "kept_grades": dict(hand_grades),
            "gold_rate": round(100.0 * hand_grades.get("Gold", 0) / num_games, 1),
            "silver_rate": round(100.0 * hand_grades.get("Silver", 0) / num_games, 1),
            "desperation_rate": round(100.0 * hand_grades.get("Desperation", 0) / num_games, 1),
            "trap_kept_rate": round(100.0 * hand_grades.get("Synergy Trap", 0) / num_games, 1),
            "rejected_grades": dict(rejected_grades),
            "traps_mulliganed_away": rejected_grades.get("Synergy Trap", 0),
        },
        "velocity_summary": {
            "commander_cast_games": len(cmd_first_cast_turns),
            "commander_cast_rate": round(100.0 * len(cmd_first_cast_turns) / num_games, 1),
            "avg_commander_cast_turn": round(sum(cmd_first_cast_turns) / len(cmd_first_cast_turns), 2) if cmd_first_cast_turns else None,
            "avg_total_commander_casts": round(sum(cmd_total_casts_per_game) / num_games, 2),
            "avg_commander_removals": round(sum(g.get("hero_commander_removed_count", 0) for g in games) / num_games, 2),
            "engine_ready_games": len(engine_ready_turns),
            "engine_ready_rate": round(100.0 * len(engine_ready_turns) / num_games, 1),
            "avg_engine_ready_turn": round(sum(engine_ready_turns) / len(engine_ready_turns), 2) if engine_ready_turns else None,
            "bracket_ready_on_time_rate": round(100.0 * ready_on_time / num_games, 1),
        },
        "combat_and_interaction": {
            "avg_combat_damage_dealt": round(sum(g.get("hero_combat_damage_dealt", 0) for g in games) / num_games, 1),
            "avg_noncombat_damage_dealt": round(sum(g.get("hero_noncombat_damage_dealt", 0) for g in games) / num_games, 1),
            "avg_commander_damage_dealt": round(sum(g.get("hero_commander_damage_dealt", 0) for g in games) / num_games, 1),
            "avg_damage_taken": round(sum(g.get("hero_damage_taken", 0) for g in games) / num_games, 1),
            "avg_permanents_lost": round(sum(g.get("hero_permanents_destroyed_or_exiled", 0) for g in games) / num_games, 1),
            "avg_interaction_fired_by_hero": round(sum(len(g.get("hero_interaction_vs_opp", [])) for g in games) / num_games, 2),
            "avg_interaction_fired_at_hero": round(sum(len(g.get("opp_interaction_vs_hero", [])) for g in games) / num_games, 2),
            "top_opp_interaction_vs_hero": opp_interaction_cards.most_common(10),
            "top_hero_interaction_vs_opp": hero_interaction_cards.most_common(10),
        },
        "card_performance": {
            "most_cast": card_cast_count.most_common(15),
            "most_drawn": card_drawn_count.most_common(15),
            "most_stranded_in_hand": card_stranded_count.most_common(12),
            "most_bottomed_on_mulligan": card_bottomed_count.most_common(10),
            "opening_hand_win_share": [
                {
                    "card": c,
                    "kept_count": cnt,
                    "wins_when_kept": card_in_winning_hand[c],
                    "win_rate": round(100.0 * card_in_winning_hand[c] / cnt, 1),
                }
                for c, cnt in card_in_kept_hand.most_common(15)
            ],
        },
        "turn_order_equity": {
            str(pos): {
                "games": turn_order_games[pos],
                "wins": turn_order_wins[pos],
                "win_rate": round(100.0 * turn_order_wins[pos] / turn_order_games[pos], 1) if turn_order_games[pos] else 0.0,
            }
            for pos in (1, 2, 3, 4)
        },
        "turn_progression": turn_progression,
        "games": games,
    }


def render_card_chip_html(card_name: str, catalog: Dict[str, Dict[str, Any]]) -> str:
    """Renders a hoverable Scryfall card link chip for HTML reports."""
    info = lookup_card_info(card_name, catalog)
    esc_name = html.escape(card_name)
    url = html.escape(info.get("scryfall_uri", f"https://scryfall.com/search?q=!{card_name.replace(' ', '+')}"))
    img = html.escape(info.get("image_uri", ""))
    data_img = f' data-img="{img}"' if img else ""
    return f'<a href="{url}" target="_blank" class="card-chip"{data_img}>{esc_name}</a>'


def generate_html_report(summary: Dict[str, Any], catalog: Dict[str, Dict[str, Any]], out_path: Path) -> None:
    """Generates the standalone interactive visual dashboard (<deck_dir>/forge_pod_report.html)."""
    oh = summary["opening_hand_summary"]
    vel = summary["velocity_summary"]
    ci = summary["combat_and_interaction"]
    cp = summary["card_performance"]

    # Pod seats table rows
    seat_rows_html = ""
    for s in summary["pod_seats_summary"]:
        badge = '<span class="badge badge-hero">HERO (SEAT 1)</span>' if s["seat"] == 1 else f'<span class="badge">SEAT {s["seat"]}</span>'
        row_cls = ' class="hero-row"' if s["seat"] == 1 else ""
        seat_rows_html += f"""
        <tr{row_cls}>
          <td>{badge}</td>
          <td><strong>{html.escape(s['deck'])}</strong><br><span class="muted">{html.escape(s['commander'])}</span></td>
          <td><strong>{s['wins']} / {summary['num_games']}</strong> ({s['win_rate']}%)</td>
          <td>{s['avg_mulligans']}</td>
          <td>{s['avg_commander_casts']}</td>
          <td>{s['avg_spells_cast']}</td>
          <td>{s['avg_peak_power']}</td>
        </tr>"""

    # Turn progression rows
    prog_rows_html = ""
    for tp in summary["turn_progression"]:
        prog_rows_html += f"""
        <tr>
          <td><strong>Turn {tp['hero_turn']}</strong></td>
          <td>{tp['games_alive']} / {summary['num_games']}</td>
          <td>{tp['avg_lands']}</td>
          <td><strong>{tp['avg_mana_ready']}</strong></td>
          <td>{tp['avg_creatures']}</td>
          <td><strong>{tp['avg_power']}</strong></td>
          <td>{tp['avg_hand_size']}</td>
          <td>{tp['avg_life']}</td>
        </tr>"""

    # Card performance tables
    most_cast_html = "".join(
        f"<tr><td>{render_card_chip_html(c, catalog)}</td><td><strong>{cnt}</strong></td><td>{round(cnt / summary['num_games'], 2)} / game</td></tr>"
        for c, cnt in cp["most_cast"]
    ) or '<tr><td colspan="3" class="muted">No spells cast</td></tr>'

    stranded_html = "".join(
        f"<tr><td>{render_card_chip_html(c, catalog)}</td><td><strong>{cnt}</strong> / {summary['num_games']} games</td><td>{lookup_card_info(c, catalog).get('cmc', '?')}</td></tr>"
        for c, cnt in cp["most_stranded_in_hand"]
    ) or '<tr><td colspan="3" class="muted">No non-land cards stranded at game end</td></tr>'

    opp_inter_html = "".join(
        f"<tr><td>{render_card_chip_html(c, catalog)}</td><td><strong>{cnt}</strong></td></tr>"
        for c, cnt in ci["top_opp_interaction_vs_hero"]
    ) or '<tr><td colspan="2" class="muted">None recorded</td></tr>'

    hero_inter_html = "".join(
        f"<tr><td>{render_card_chip_html(c, catalog)}</td><td><strong>{cnt}</strong></td></tr>"
        for c, cnt in ci["top_hero_interaction_vs_opp"]
    ) or '<tr><td colspan="2" class="muted">None recorded</td></tr>'

    # Per-game accordion logs
    games_html = ""
    for g in summary["games"]:
        g_idx = g["game_index"]
        hero_won = (g.get("winner_seat") == 1)
        win_badge = (
            '<span class="badge badge-gold">HERO VICTORY</span>'
            if hero_won
            else f'<span class="badge badge-loss">WINNER: {html.escape(g.get("winner_deck", "DRAW"))}</span>'
        )
        eval_info = g.get("hero_kept_hand_eval", {})
        grade = eval_info.get("grade", "Silver")
        grade_cls = "badge-gold" if grade == "Gold" else ("badge- silver" if grade == "Silver" else "badge-loss")

        kept_chips = " ".join(render_card_chip_html(c, catalog) for c in g.get("hero_kept_hand", []))

        mull_section = ""
        if g.get("hero_mulliganed_evals"):
            m_items = []
            for idx_m, m_obj in enumerate(g["hero_mulliganed_evals"], start=1):
                m_chips = " ".join(render_card_chip_html(c, catalog) for c in m_obj["hand"])
                m_grade = m_obj["eval"]["grade"]
                m_items.append(f'<div class="sub-box"><strong>Rejected Hand #{idx_m} ({html.escape(m_grade)}):</strong> {m_chips}</div>')
            if g.get("hero_bottomed_cards"):
                b_chips = " ".join(render_card_chip_html(c, catalog) for c in g["hero_bottomed_cards"])
                m_items.append(f'<div class="sub-box"><strong>London Mulligan Bottomed:</strong> {b_chips}</div>')
            mull_section = "".join(m_items)

        draws_by_t: Dict[int, List[str]] = defaultdict(list)
        for dr in g.get("hero_draws", []):
            draws_by_t[dr["hero_turn"]].append(dr["card"])

        opp_vs_by_t: Dict[int, List[str]] = defaultdict(list)
        for ir in g.get("opp_interaction_vs_hero", []):
            opp_vs_by_t[ir["hero_turn"]].append(f"{ir['by_player']} -> {ir['card']} ({ir['targets']})")

        turn_rows = ""
        for snap in g.get("hero_turn_snapshots", []):
            ht = snap["hero_turn"]
            drawn_chips = " ".join(render_card_chip_html(c, catalog) for c in draws_by_t.get(ht, [])) or '<span class="muted">—</span>'
            actions_str = " | ".join(html.escape(a) for a in snap.get("actions_this_turn", [])) or '<span class="muted">(pass)</span>'
            opp_str = "<br>".join(html.escape(x) for x in opp_vs_by_t.get(ht, []))
            if opp_str:
                actions_str += f'<br><span style="color:#f87171;">⚠️ Targeted by: {opp_str}</span>'
            turn_rows += f"""
            <tr>
              <td><strong>T{ht}</strong> <span class="muted">(G{snap['global_turn']})</span></td>
              <td>{drawn_chips}</td>
              <td>{actions_str}</td>
              <td>{snap['lands_total']} ({snap['mana_sources_ready']} ready)</td>
              <td>{snap['creatures_count']} ({snap['total_power']} pwr)</td>
              <td>{snap['hand_size']}</td>
              <td>{snap['hero_life']}</td>
            </tr>"""

        final_hand_chips = " ".join(render_card_chip_html(c, catalog) for c in g.get("hero_final_hand", [])) or '<span class="muted">Empty hand</span>'

        games_html += f"""
        <details class="game-card" {"open" if g_idx == 1 else ""}>
          <summary>
            <span><strong>Game #{g_idx}</strong> — {win_badge} — <span class=" badge {grade_cls}">{html.escape(grade)} Keep ({g.get('hero_opening_hand_size', 7)} cards, {g.get('hero_mulligans', 0)} mull)</span></span>
            <span class="muted">Turn Order #{g.get('hero_turn_order_pos', 1)} | {g.get('total_hero_turns', 0)} Hero Turns ({g.get('total_global_turns', 0)} Global) | {round(g.get('duration_ms', 0)/1000.0, 1)}s</span>
          </summary>
          <div class="game-body">
            <div class="sub-box"><strong>Final Kept Opening Hand ({g.get('hero_opening_hand_size', 7)} cards — {html.escape(grade)}):</strong> {kept_chips}</div>
            {mull_section}
            <table class="data-table compact">
              <thead>
                <tr>
                  <th>Turn</th>
                  <th>Cards Drawn</th>
                  <th>Plays &amp; Opponent Interaction</th>
                  <th>Lands (Mana)</th>
                  <th>Board (Power)</th>
                  <th>Hand</th>
                  <th>Life</th>
                </tr>
              </thead>
              <tbody>{turn_rows}</tbody>
            </table>
            <div class="sub-box" style="margin-top:8px;"><strong>Cards Remaining in Hand at Game End:</strong> {final_hand_chips}</div>
          </div>
        </details>"""

    avg_cmd_t = f"Turn {vel['avg_commander_cast_turn']}" if vel["avg_commander_cast_turn"] else "Not Cast"
    avg_rdy_t = f"Turn {vel['avg_engine_ready_turn']}" if vel["avg_engine_ready_turn"] else "Not Reached"

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forge 4-AI Pod Telemetry — {html.escape(summary['hero_deck'])}</title>
<style>
  :root {{
    --bg: #0f172a;
    --panel: #1e293b;
    --border: #334155;
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --gold: #fbbf24;
    --green: #4ade80;
    --red: #f87171;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 28px;
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.5;
  }}
  .container {{ max-width: 1380px; margin: 0 auto; }}
  .header {{
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 24px; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;
  }}
  h1 {{ margin: 0 0 6px 0; font-size: 1.75rem; color: #fff; }}
  h2 {{ margin: 0 0 14px 0; font-size: 1.2rem; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
  .muted {{ color: var(--muted); font-size: 0.88rem; }}
  .kpi-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px; margin-bottom: 24px;
  }}
  .kpi-card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 10px; padding: 16px;
  }}
  .kpi-label {{ color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}
  .kpi-val {{ font-size: 1.65rem; font-weight: 700; margin: 6px 0 2px 0; color: #fff; }}
  .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap: 20px; margin-bottom: 24px; }}
  .panel {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin-bottom: 24px; }}
  .data-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  .data-table th, .data-table td {{ padding: 9px 12px; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }}
  .data-table th {{ color: var(--muted); font-weight: 600; font-size: 0.8rem; text-transform: uppercase; background: rgba(15,23,42,0.5); }}
  .data-table.compact th, .data-table.compact td {{ padding: 6px 9px; font-size: 0.84rem; }}
  .hero-row {{ background: rgba(56, 189, 248, 0.08); }}
  .badge {{
    display: inline-block; padding: 2px 8px; border-radius: 999px;
    font-size: 0.75rem; font-weight: 600; background: #334155; color: #e2e8f0;
  }}
  .badge-hero {{ background: #0284c7; color: #fff; }}
  .badge-gold {{ background: rgba(251, 191, 36, 0.2); color: var(--gold); border: 1px solid rgba(251, 191, 36, 0.4); }}
  .badge-loss {{ background: rgba(248, 113, 113, 0.18); color: var(--red); border: 1px solid rgba(248, 113, 113, 0.35); }}
  .card-chip {{
    display: inline-block; padding: 2px 8px; margin: 2px;
    background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 6px; color: var(--accent); text-decoration: none; font-size: 0.82rem;
  }}
  .card-chip:hover {{ background: rgba(56, 189, 248, 0.25); color: #fff; }}
  .game-card {{
    background: rgba(15, 23, 42, 0.55); border: 1px solid var(--border);
    border-radius: 8px; margin-bottom: 12px; overflow: hidden;
  }}
  .game-card summary {{
    padding: 12px 16px; cursor: pointer; display: flex; justify-content: space-between; align-items: center;
    background: rgba(30, 41, 59, 0.9); user-select: none;
  }}
  .game-body {{ padding: 14px 16px; border-top: 1px solid var(--border); }}
  .sub-box {{ background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border); border-radius: 6px; padding: 8px 12px; margin-bottom: 10px; font-size: 0.86rem; }}
  #card-preview {{
    position: fixed; display: none; z-index: 9999; pointer-events: none;
    width: 240px; border-radius: 12px; box-shadow: 0 14px 30px rgba(0,0,0,0.75); border: 2px solid var(--accent);
  }}
</style>
</head>
<body>
<img id="card-preview" src="" alt="Card Preview" />
<div class="container">
  <div class="header">
    <div>
      <h1>MTG Forge 4-AI Commander Pod Telemetry: {html.escape(summary['hero_deck'])}</h1>
      <div class="muted">Commander: <strong>{html.escape(summary['hero_commander'])}</strong> &bull; Target: <strong>{html.escape(summary['bracket_label'])} (T{summary['target_turn']})</strong> &bull; Simulated {summary['num_games']} Full Games in {summary['wall_clock_sec']}s</div>
    </div>
    <div>
      <span class="badge badge-hero" style="font-size:0.9rem;padding:6px 14px;">Hero Win Rate: {summary['hero_win_rate']}% ({summary['hero_wins']}/{summary['num_games']})</span>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Hero Pod Win Rate</div>
      <div class="kpi-val" style="color:var(--green);">{summary['hero_win_rate']}%</div>
      <div class="muted">{summary['hero_wins']} wins / {summary['num_games']} games (25% baseline)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Opening Hand Quality</div>
      <div class="kpi-val" style="color:var(--gold);">{oh['gold_rate']}% Gold</div>
      <div class="muted">{oh['silver_rate']}% Silver &bull; {oh['desperation_rate']}% Desp &bull; {oh['traps_mulliganed_away']} Traps Mulled</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Hand Size / Mulls</div>
      <div class="kpi-val">{oh['avg_starting_hand_size']} cards</div>
      <div class="muted">Avg {oh['avg_mulligans']} mulligans / game</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Commander Deployment</div>
      <div class="kpi-val" style="color:var(--accent);">{avg_cmd_t}</div>
      <div class="muted">Cast in {vel['commander_cast_rate']}% of games ({vel['avg_total_commander_casts']}x/game)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Engine Readiness</div>
      <div class="kpi-val">{avg_rdy_t}</div>
      <div class="muted">{vel['bracket_ready_on_time_rate']}% on time (&le; T{summary['target_turn']})</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Avg Game Length</div>
      <div class="kpi-val">{summary['avg_hero_turns']} Rounds</div>
      <div class="muted">{summary['avg_global_turns']} player turns ({summary['avg_game_duration_sec']}s CPU/game)</div>
    </div>
  </div>

  <div class="panel">
    <h2>4-Seat Gauntlet Pod Standings</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Seat</th>
          <th>Deck &amp; Commander</th>
          <th>Wins (Win Rate)</th>
          <th>Avg Mulligans</th>
          <th>Avg Cmd Casts</th>
          <th>Avg Spells Cast</th>
          <th>Avg Peak Board Power</th>
        </tr>
      </thead>
      <tbody>{seat_rows_html}</tbody>
    </table>
  </div>

  <div class="panel">
    <h2>Seat 1 (Hero) Turn-by-Turn Resource &amp; Board Progression</h2>
    <table class="data-table">
      <thead>
        <tr>
          <th>Hero Turn</th>
          <th>Games Alive</th>
          <th>Avg Lands</th>
          <th>Avg Ready Mana Sources</th>
          <th>Avg Creatures</th>
          <th>Avg Total Power</th>
          <th>Avg Hand Size</th>
          <th>Avg Life Total</th>
        </tr>
      </thead>
      <tbody>{prog_rows_html}</tbody>
    </table>
  </div>

  <div class="grid-2">
    <div class="panel" style="margin-bottom:0;">
      <h2>Most Cast Hero Spells</h2>
      <table class="data-table compact">
        <thead><tr><th>Card</th><th>Total Casts</th><th>Frequency</th></tr></thead>
        <tbody>{most_cast_html}</tbody>
      </table>
    </div>
    <div class="panel" style="margin-bottom:0;">
      <h2>Most Stranded Non-Land Cards in Hand at Game End</h2>
      <table class="data-table compact">
        <thead><tr><th>Card</th><th>Stranded Games</th><th>CMC</th></tr></thead>
        <tbody>{stranded_html}</tbody>
      </table>
    </div>
  </div>

  <div class="grid-2" style="margin-top:24px;">
    <div class="panel" style="margin-bottom:0;">
      <h2>Opponent Targeted Interaction Fired at Hero ({ci['avg_interaction_fired_at_hero']}/game)</h2>
      <table class="data-table compact">
        <thead><tr><th>Opponent Card</th><th>Times Fired at Hero</th></tr></thead>
        <tbody>{opp_inter_html}</tbody>
      </table>
    </div>
    <div class="panel" style="margin-bottom:0;">
      <h2>Hero Targeted Interaction Fired at Opponents ({ci['avg_interaction_fired_by_hero']}/game)</h2>
      <table class="data-table compact">
        <thead><tr><th>Hero Card</th><th>Times Fired</th></tr></thead>
        <tbody>{hero_inter_html}</tbody>
      </table>
    </div>
  </div>

  <div class="panel" style="margin-top:24px;">
    <h2>Game-by-Game Full Telemetry Replays (Opening Hands, Draws, Plays &amp; Board States)</h2>
    {games_html}
  </div>
</div>
<script>
  const preview = document.getElementById('card-preview');
  document.querySelectorAll('.card-chip[data-img]').forEach(el => {{
    el.addEventListener('mouseenter', e => {{
      const img = el.getAttribute('data-img');
      if (img) {{
        preview.src = img;
        preview.style.display = 'block';
      }}
    }});
    el.addEventListener('mousemove', e => {{
      let x = e.clientX + 20;
      let y = e.clientY - 60;
      if (x + 260 > window.innerWidth) x = e.clientX - 260;
      if (y + 340 > window.innerHeight) y = window.innerHeight - 350;
      if (y < 10) y = 10;
      preview.style.left = x + 'px';
      preview.style.top = y + 'px';
    }});
    el.addEventListener('mouseleave', () => {{
      preview.style.display = 'none';
    }});
  }});
</script>
</body>
</html>"""
    out_path.write_text(html_doc, encoding="utf-8")


def generate_markdown_report(summary: Dict[str, Any]) -> str:
    """Formats a concise Markdown summary suitable for console and FORGE_POD_LOG.md."""
    oh = summary["opening_hand_summary"]
    vel = summary["velocity_summary"]
    ci = summary["combat_and_interaction"]
    cp = summary["card_performance"]

    lines = [
        f"## [{summary['date']}] — Headless Forge 4-AI Pod Simulation ({summary['num_games']} games, {summary['bracket_label']})",
        "",
        f"- **Hero Deck (Seat 1):** `{summary['hero_deck']}` (**{summary['hero_commander']}**)",
        f"- **Execution Time:** `{summary['wall_clock_sec']}s` wall-clock (`{summary['avg_game_duration_sec']}s` avg CPU/game across {summary['num_games']} games)",
        f"- **Pod Win Rate:** **{summary['hero_win_rate']}%** ({summary['hero_wins']} / {summary['num_games']} wins vs. 25.0% 4-seat baseline)",
        f"- **Opening Hand Quality:** **{oh['gold_rate']}% Gold** | **{oh['silver_rate']}% Silver** | **{oh['desperation_rate']}% Desperation** (Avg Hand Size: `{oh['avg_starting_hand_size']}`, Avg Mulligans: `{oh['avg_mulligans']}`, Synergy Traps Mulled: `{oh['traps_mulliganed_away']}`)",
        f"- **Commander & Engine Velocity:** Commander Cast Rate **{vel['commander_cast_rate']}%** (Avg Turn: `{vel['avg_commander_cast_turn']}`, Avg Total Casts: `{vel['avg_total_commander_casts']}`, Removed: `{vel['avg_commander_removals']}`/game) | Engine Readiness: **{vel['engine_ready_rate']}%** (Avg Turn: `{vel['avg_engine_ready_turn']}`, On-Time $\\le$ T{summary['target_turn']}: **{vel['bracket_ready_on_time_rate']}%**)",
        f"- **Combat & Interaction:** Avg Combat Damage Dealt: `{ci['avg_combat_damage_dealt']}` (Cmdr: `{ci['avg_commander_damage_dealt']}`), Non-Combat Damage: `{ci['avg_noncombat_damage_dealt']}` | Targeted Removal Fired by Hero: `{ci['avg_interaction_fired_by_hero']}`/game, Fired at Hero: `{ci['avg_interaction_fired_at_hero']}`/game",
        "",
        "### 4-Seat Pod Standings",
        "| Seat | Deck | Commander | Wins | Win Rate | Avg Mulls | Avg Cmd Casts | Avg Spells Cast | Avg Peak Power |",
        "| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    for s in summary["pod_seats_summary"]:
        lines.append(
            f"| {s['seat']} | **{s['deck']}** | {s['commander']} | {s['wins']}/{summary['num_games']} | **{s['win_rate']}%** | {s['avg_mulligans']} | {s['avg_commander_casts']} | {s['avg_spells_cast']} | {s['avg_peak_power']} |"
        )

    lines.extend([
        "",
        "### Seat 1 (Hero) Turn-by-Turn Progression",
        "| Turn | Games Alive | Avg Lands | Avg Ready Mana | Avg Creatures | Avg Board Power | Avg Hand Size | Avg Life |",
        "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ])
    for tp in summary["turn_progression"][:10]:
        lines.append(
            f"| **T{tp['hero_turn']}** | {tp['games_alive']}/{summary['num_games']} | {tp['avg_lands']} | **{tp['avg_mana_ready']}** | {tp['avg_creatures']} | **{tp['avg_power']}** | {tp['avg_hand_size']} | {tp['avg_life']} |"
        )

    if cp["most_stranded_in_hand"]:
        stranded_str = ", ".join(f"**{c}** ({cnt}x)" for c, cnt in cp["most_stranded_in_hand"][:6])
        lines.append(f"\n- **Most Stranded Non-Land Cards at Game End:** {stranded_str}")

    if cp["most_cast"]:
        cast_str = ", ".join(f"**{c}** ({cnt}x)" for c, cnt in cp["most_cast"][:8])
        lines.append(f"- **Most Frequently Cast Hero Spells:** {cast_str}")

    lines.append("")
    return "\n".join(lines)


def handle_remote_cluster_admin(remote_url: str, check_only: bool, update_mode: Optional[str]):
    """Checks for updates or triggers self-updating on the remote forgesim.chayde.lab cluster."""
    base = remote_url.rstrip("/")
    if check_only:
        url = f"{base}/api/v1/check-update"
        print(f"[*] Checking remote cluster update status at {url} ...")
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(data, indent=2))
        return

    if update_mode:
        url = f"{base}/api/v1/update"
        payload: Dict[str, Any] = {"mode": update_mode}
        if update_mode == "push":
            java_code = BRIDGE_JAVA.read_text(encoding="utf-8")
            commit_sha = ""
            try:
                res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=3)
                if res.returncode == 0:
                    commit_sha = res.stdout.strip()
            except Exception:
                pass
            payload["java_source"] = java_code
            payload["commit"] = commit_sha
            ver_file = REPO_ROOT / "forgesim_cluster" / "version.json"
            srv_file = REPO_ROOT / "forgesim_cluster" / "forgesim_server.py"
            if ver_file.exists():
                payload["version_json"] = ver_file.read_text(encoding="utf-8")
            if srv_file.exists():
                payload["server_source"] = srv_file.read_text(encoding="utf-8")
            print(f"[*] Pushing local ForgePodRunner.java, forgesim_server.py & version.json to {url} ...")
        else:
            print(f"[*] Triggering remote cluster update (mode={update_mode}) at {url} ...")

        raw_body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=raw_body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(data, indent=2))


def run_remote_cluster_batch(
    remote_url: str,
    forge_cmd_dir: Path,
    pod_dcks: List[str],
    num_games: int,
    timeout_sec: int,
    ai_timeout_sec: int,
    base_seed: int,
    smart_mulligan: bool,
) -> List[Dict[str, Any]]:
    """
    Sends raw .dck contents for all 4 seats to the remote `forgesim.chayde.lab` cluster
    service (`POST /api/v1/simulate`) and returns the array of game telemetry objects.
    """
    base = remote_url.rstrip("/")
    decks_payload = []
    for dck_name in pod_dcks:
        dck_path = forge_cmd_dir / dck_name
        if not dck_path.exists():
            raise FileNotFoundError(f"Deck file not found for remote payload: {dck_path}")
        decks_payload.append({
            "name": dck_path.stem,
            "dck_content": dck_path.read_text(encoding="utf-8", errors="replace"),
        })

    req_payload = {
        "decks": decks_payload,
        "games": num_games,
        "timeout": timeout_sec,
        "ai_timeout": ai_timeout_sec,
        "seed": base_seed,
        "smart_mulligan": smart_mulligan,
    }
    raw_body = json.dumps(req_payload).encode("utf-8")
    sim_url = f"{base}/api/v1/simulate"
    req = urllib.request.Request(
        sim_url,
        data=raw_body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    http_timeout = max(120, num_games * timeout_sec + 60)
    with urllib.request.urlopen(req, timeout=http_timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("status") != "ok":
        raise RuntimeError(f"Remote cluster returned error: {data.get('error', data)}")
    return data.get("games", [])


def main():
    parser = argparse.ArgumentParser(
        description="Run headless 4-AI Commander pod simulations in MTG Forge with full Seat 1 hand/draw telemetry."
    )
    parser.add_argument("deck", nargs="?", default=None, help="Target Hero deck (repo folder path, deck name, or .dck file)")
    parser.add_argument(
        "--pod",
        nargs="+",
        help="3 opponent decks for Seats 2, 3, and 4 (defaults to preset gauntlet)",
    )
    parser.add_argument(
        "--gauntlet",
        choices=list(DEFAULT_GAUNTLETS.keys()),
        default="bracket3",
        help="Preset opponent gauntlet if --pod is not specified (default: bracket3)",
    )
    parser.add_argument("--games", "-n", type=int, default=4, help="Total number of full games to simulate (default: 4)")
    parser.add_argument("--workers", "-w", type=int, default=2, help="Parallel local JVM worker processes (default: 2)")
    parser.add_argument("--timeout", "-c", type=int, default=90, help="Per-game clock timeout in seconds (default: 90)")
    parser.add_argument("--ai-timeout", type=int, default=2, help="Per-decision AI combat timeout in seconds (default: 2)")
    parser.add_argument("--bracket", "-b", type=int, default=3, choices=[1, 2, 3, 4, 5], help="Target Commander Bracket 1-5 (default: 3)")
    parser.add_argument("--seed", "-s", type=int, default=None, help="Optional base RNG seed for reproducibility")
    parser.add_argument("--stock-mulligan", action="store_true", help="Use stock Forge mulligan instead of Smart Synergy-Aware Mulligan")
    parser.add_argument(
        "--remote",
        nargs="?",
        const=os.environ.get("FORGESIM_URL", "http://forgesim.chayde.lab"),
        default=os.environ.get("FORGESIM_URL"),
        help="Offload simulation to the homelab cluster service (default URL: http://forgesim.chayde.lab)",
    )
    parser.add_argument("--local", action="store_true", help="Force local JVM execution even if FORGESIM_URL is set")
    parser.add_argument("--check-remote-update", action="store_true", help="Check if the remote homelab cluster has an update available")
    parser.add_argument(
        "--update-remote",
        nargs="?",
        const="push",
        choices=["push", "github", "watchtower"],
        help="Update the remote homelab cluster ('push' local Java bridge, pull from 'github', or trigger 'watchtower')",
    )

    args = parser.parse_args()

    remote_target = None if args.local else args.remote
    if args.check_remote_update or args.update_remote:
        target_url = remote_target or "http://forgesim.chayde.lab"
        handle_remote_cluster_admin(target_url, args.check_remote_update, args.update_remote)
        return

    if not args.deck:
        parser.error("the following arguments are required: deck (unless using --check-remote-update or --update-remote)")

    forge_cmd_dir = stf.get_default_forge_commander_dir()
    if not forge_cmd_dir or not forge_cmd_dir.exists():
        raise FileNotFoundError("Could not locate %APPDATA%/Forge/decks/commander directory.")

    forge_dir: Optional[Path] = None
    forge_jar: Optional[Path] = None
    bridge_dir: Optional[Path] = None
    if not remote_target:
        forge_dir, forge_jar = find_forge_install()
        bridge_dir = ensure_bridge_compiled(forge_jar)

    hero_dck, hero_repo_dir = resolve_deck_to_dck(args.deck, forge_cmd_dir)

    # Resolve 3 Opponent Gauntlet decks
    opp_specs = args.pod if args.pod else list(DEFAULT_GAUNTLETS[args.gauntlet])
    opp_dcks: List[str] = []
    for spec in opp_specs:
        dck_name, _ = resolve_deck_to_dck(spec, forge_cmd_dir)
        if dck_name.lower() == hero_dck.lower():
            # Substitute from fallback pool so Hero doesn't play a mirror match unless explicitly requested via --pod
            if not args.pod:
                for fb in FALLBACK_POOL:
                    fb_dck, _ = resolve_deck_to_dck(fb, forge_cmd_dir)
                    if fb_dck.lower() != hero_dck.lower() and fb_dck not in opp_dcks:
                        dck_name = fb_dck
                        break
        opp_dcks.append(dck_name)

    while len(opp_dcks) < 3:
        for fb in FALLBACK_POOL:
            fb_dck, _ = resolve_deck_to_dck(fb, forge_cmd_dir)
            if fb_dck.lower() != hero_dck.lower() and fb_dck not in opp_dcks:
                opp_dcks.append(fb_dck)
                if len(opp_dcks) == 3:
                    break

    pod_dcks = [hero_dck] + opp_dcks[:3]

    mode_str = f"REMOTE CLUSTER ({remote_target})" if remote_target else f"LOCAL ({min(args.workers, args.games)} workers)"
    print(f"======================================================================")
    print(f"MTG FORGE 4-AI COMMANDER POD SIMULATOR (WITH JAVA TELEMETRY BRIDGE)")
    print(f"  Execution Mode: {mode_str}")
    print(f"  Seat 1 (Hero) : {pod_dcks[0]}")
    print(f"  Seat 2 (Opp 1): {pod_dcks[1]}")
    print(f"  Seat 3 (Opp 2): {pod_dcks[2]}")
    print(f"  Seat 4 (Opp 3): {pod_dcks[3]}")
    print(f"  Config        : {args.games} games | {args.timeout}s cap | Bracket {args.bracket}")
    print(f"======================================================================")

    catalog = load_hero_card_catalog(hero_repo_dir, forge_cmd_dir / hero_dck)
    base_seed = args.seed if args.seed is not None else int(time.time() * 1000) % 1_000_000_000

    t0 = time.perf_counter()
    all_games: List[Dict[str, Any]] = []

    if remote_target:
        try:
            all_games = run_remote_cluster_batch(
                remote_target,
                forge_cmd_dir,
                pod_dcks,
                args.games,
                args.timeout,
                args.ai_timeout,
                base_seed,
                not args.stock_mulligan,
            )
        except Exception as rem_err:
            print(f"[WARN] Remote cluster dispatch to {remote_target} failed ({rem_err}). Falling back to local execution...", file=sys.stderr)
            remote_target = None
            forge_dir, forge_jar = find_forge_install()
            bridge_dir = ensure_bridge_compiled(forge_jar)

    if not remote_target:
        num_workers = max(1, min(args.workers, args.games))
        worker_counts = [args.games // num_workers] * num_workers
        for i in range(args.games % num_workers):
            worker_counts[i] += 1

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as pool:
            futures = []
            seed_offset = 0
            for w_idx, count in enumerate(worker_counts):
                if count <= 0:
                    continue
                futures.append(
                    pool.submit(
                        run_worker_batch,
                        w_idx + 1,
                        forge_dir,
                        forge_jar,
                        bridge_dir,
                        forge_cmd_dir,
                        pod_dcks,
                        count,
                        args.timeout,
                        args.ai_timeout,
                        base_seed + seed_offset * 1000,
                        not args.stock_mulligan,
                    )
                )
                seed_offset += 1

            for fut in concurrent.futures.as_completed(futures):
                batch_games = fut.result()
                all_games.extend(batch_games)

    wall_clock = time.perf_counter() - t0
    summary = enrich_and_aggregate(all_games, catalog, args.bracket, pod_dcks, wall_clock)

    md_report = generate_markdown_report(summary)
    print("\n" + md_report)

    out_dir = hero_repo_dir if hero_repo_dir else (REPO_ROOT / "logs")
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "forge_pod_results.json"
    html_path = out_dir / "forge_pod_report.html"
    md_path = out_dir / "FORGE_POD_LOG.md"

    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    generate_html_report(summary, catalog, html_path)

    if md_path.exists():
        existing = md_path.read_text(encoding="utf-8")
        md_path.write_text(existing.rstrip() + "\n\n---\n\n" + md_report, encoding="utf-8")
    else:
        md_path.write_text(f"# MTG Forge 4-AI Pod Simulation Log — {summary['hero_deck']}\n\n" + md_report, encoding="utf-8")

    print(f"Saved Reports:")
    print(f"  - HTML Dashboard : {html_path}")
    print(f"  - Markdown Log   : {md_path}")
    print(f"  - Raw Telemetry  : {json_path}")


if __name__ == "__main__":
    main()
