#!/usr/bin/env python3
"""
scripts/minnow_prep.py — Elephant-Minnow Model (EMM) Blind Spec Packer, Drift Detector & Visual Report Renderer

Implements the deterministic tooling layer for the MTG Elephant-Minnow Model (adapted from
Google's Elephant-Goldfish Model, https://github.com/google/elephant-goldfish-model):

1. --pack: Generates `<deck_dir>/minnow_blind_spec.txt` — a strictly prose-stripped, unbiased
   100-card Scryfall Oracle dossier for zero-context Minnow subagents (enforcing the Information Firewall).
2. --drift: Executes `emm-drift-report` across `<deck_dir>` (or `--all`), comparing:
   - `moxfield_import.txt`
   - Main `.md` `Plain Text Copy/Paste` (including 2-trailing-space GFM check)
   - Main `.md` `Card Explanations` bullets (catching ghost cards left in prose after swaps)
   - `dti_eval.json` card ledger references
   - MTG Forge `.dck` synchronization status
3. --render: Renders `<deck_dir>/minnow_eval.json` into `<deck_dir>/minnow_review_report.md` and
   an interactive dark-mode visual dashboard `<deck_dir>/minnow_report.html`.

Usage:
  python scripts/minnow_prep.py "commander_decks/Planning/ObekaSplitterOfSeconds" --pack
  python scripts/minnow_prep.py "commander_decks/Planning/ObekaSplitterOfSeconds" --drift
  python scripts/minnow_prep.py --drift --all
  python scripts/minnow_prep.py "commander_decks/Planning/ObekaSplitterOfSeconds" --render
"""

import os
import re
import sys
import json
import html
import argparse
import urllib.parse
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set, Any

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scryfall_lookup import lookup_named
from sync_to_forge import get_default_forge_commander_dir, determine_forge_deck_name

# Known filter lands and filter rocks (Signets) flagged by player preference rules
BANNED_FILTER_ROCKS = {
    "azorius signet", "boros signet", "dimir signet", "golgari signet", "gruul signet",
    "izzet signet", "orzhov signet", "rakdos signet", "selesnya signet", "simic signet",
}
BANNED_FILTER_LANDS = {
    "skycloud expanse", "darkwater catacombs", "shadowblood ridge", "mossfire valley",
    "sungrass prairie", "desolate mire", "fertile thicket", "viridescent bog",
    "sunscorched divide", "overflowing basin", "mystic gate", "sunken ruins",
    "graven cairns", "fire-lit thicket", "wooded bastion", "fetid heath",
    "cascade bluffs", "twilight mire", "rugged prairie", "flooded grove",
}
KNOWN_MLD_CARDS = {
    "armageddon", "ravages of war", "catastrophe", "jokulhaups", "obliterate",
    "decree of annihilation", "sunder", "blood moon", "magus of the moon",
    "winter orb", "static orb", "stasis", "back to basics", "ruination",
    "from the ashes", "wave of vitriol", "contamination", "infernal darkness",
    "hall of gemstone", "vorinclex, voice of hunger",
}


def normalize_card_name(name: str) -> str:
    """Normalizes a card name for comparison across files."""
    s = name.strip()
    s = re.sub(r'\s*\*[A-Za-z0-9_-]+\*', '', s)
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    if " // " in s:
        s = s.split(" // ")[0].strip()
    elif " / " in s:
        s = s.split(" / ")[0].strip()
    return s.lower()


def find_main_md_file(deck_dir: Path) -> Optional[Path]:
    """Locates the primary deck guide .md file in a deck directory."""
    excluded = {
        "order_tracking.md", "goldfish_log.md", "goldfish_log_old.md",
        "dti_audit.md", "advertised_decklist.md", "minnow_review_report.md",
        "concepts_brief.md", "design_draft.md", "drift_report.md",
        "originalprompt.md", "price_analysis.md", "deck_analysis.md",
        "mechanics.md", "sideboard_analysis.md", "optimization_log.md",
    }
    md_files = [
        f for f in sorted(deck_dir.glob("*.md"))
        if f.name.lower() not in excluded and not f.name.lower().endswith(".old.md")
    ]
    if not md_files:
        return None

    # Prefer file with deck_status: main in YAML frontmatter
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")[:500]
            if "deck_status: main" in text:
                return f
        except Exception:
            pass

    # Next prefer non-README file if another guide exists
    non_readme = [f for f in md_files if f.name.lower() != "readme.md"]
    if non_readme:
        return non_readme[0]
    return md_files[0]


def parse_moxfield_file(mox_path: Path) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str]]]:
    """
    Parses moxfield_import.txt into (commanders, mainboard) as lists of (qty, card_name).
    """
    commanders: List[Tuple[int, str]] = []
    mainboard: List[Tuple[int, str]] = []
    if not mox_path.exists():
        return commanders, mainboard

    section = "main"
    for raw_line in mox_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("---") or line.startswith("* "):
            continue
        header_key = re.sub(r'[^a-z0-9]', '', line.lower())
        if header_key in {"commander", "commanders"}:
            section = "commander"
            continue
        elif header_key in {"deck", "main", "maindeck", "mainboard"}:
            section = "main"
            continue
        elif header_key in {"sideboard", "maybeboard"}:
            section = "sideboard"
            continue

        is_cmdr = "*cmdr*" in line.lower()
        cleaned = re.sub(r'\s*\*[A-Za-z0-9_-]+\*', '', line).strip()
        cleaned = cleaned.replace("\u2019", "'").replace("\u2018", "'")
        m = re.match(r'^(\d+)\s+(.+)$', cleaned)
        if not m:
            continue
        qty = int(m.group(1))
        cname = m.group(2).strip()
        if "token" in cname.lower() or "emblem" in cname.lower() or cname.lower() == "the ring tempts you":
            continue

        if section == "commander" or is_cmdr:
            commanders.append((qty, cname))
        elif section == "main":
            mainboard.append((qty, cname))

    if not commanders and mainboard:
        commanders.append(mainboard.pop(0))

    return commanders, mainboard


def pack_blind_spec(
    deck_dir: Path,
    in_cards: Optional[List[str]] = None,
    out_cards: Optional[List[str]] = None,
    target_bracket: Optional[int] = None,
) -> Path:
    """
    Creates `<deck_dir>/minnow_blind_spec.txt` containing ONLY verified Scryfall card data
    and aggregate mathematical counts (zero prose commentary, zero strategy sales pitch).
    """
    mox_path = deck_dir / "moxfield_import.txt"
    if not mox_path.exists():
        raise FileNotFoundError(f"Could not find {mox_path}")

    commanders, mainboard = parse_moxfield_file(mox_path)

    # Detect target bracket from main .md or dti_eval.json if not explicitly passed
    if target_bracket is None:
        dti_path = deck_dir / "dti_eval.json"
        if dti_path.exists():
            try:
                dti_data = json.loads(dti_path.read_text(encoding="utf-8"))
                target_bracket = dti_data.get("target_bracket")
            except Exception:
                pass
        if target_bracket is None:
            md_file = find_main_md_file(deck_dir)
            if md_file:
                md_text = md_file.read_text(encoding="utf-8", errors="ignore")
                bm = re.search(r'Bracket\s*([1-5])', md_text, re.IGNORECASE)
                if bm:
                    target_bracket = int(bm.group(1))

    all_entries = [("COMMANDER", qty, name) for qty, name in commanders] + [
        ("MAINBOARD", qty, name) for qty, name in mainboard
    ]

    card_records: List[Dict[str, Any]] = []
    game_changers: List[str] = []
    mld_cards: List[str] = []
    filter_violations: List[str] = []
    type_buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    cmc_curve: Dict[int, int] = defaultdict(int)
    pip_counts: Dict[str, int] = defaultdict(int)
    total_cards = 0
    land_count = 0
    nonland_cmc_sum = 0.0
    nonland_count = 0

    for zone, qty, raw_name in all_entries:
        total_cards += qty
        data = lookup_named(raw_name)
        if not data:
            rec = {
                "zone": zone,
                "qty": qty,
                "name": raw_name,
                "mana_cost": "?",
                "cmc": 0,
                "type_line": "Unknown",
                "oracle_text": "[Scryfall lookup failed]",
                "pt": "",
                "game_changer": False,
                "color_identity": [],
            }
            card_records.append(rec)
            type_buckets["Other"].append(rec)
            continue

        # Handle DFCs
        faces = data.get("card_faces", [])
        if faces and not data.get("oracle_text"):
            mana_cost = " // ".join(f.get("mana_cost", "") for f in faces if f.get("mana_cost"))
            type_line = data.get("type_line") or " // ".join(f.get("type_line", "") for f in faces)
            oracle_parts = []
            for f in faces:
                f_pt = f" ({f['power']}/{f['toughness']})" if "power" in f and "toughness" in f else ""
                oracle_parts.append(f"[{f.get('name', '')}{f_pt}]: {f.get('oracle_text', '')}")
            oracle_text = " // ".join(oracle_parts)
            pt = f"{faces[0].get('power')}/{faces[0].get('toughness')}" if "power" in faces[0] else ""
        else:
            mana_cost = data.get("mana_cost", "")
            type_line = data.get("type_line", "")
            oracle_text = data.get("oracle_text", "").replace("\n", " | ")
            pt = f"{data.get('power')}/{data.get('toughness')}" if "power" in data and "toughness" in data else ""

        cmc = float(data.get("cmc", 0))
        is_gc = bool(data.get("game_changer", False))
        ci = data.get("color_identity", [])
        clean_name = data.get("name", raw_name)

        if is_gc:
            game_changers.append(clean_name)
        if normalize_card_name(clean_name) in KNOWN_MLD_CARDS:
            mld_cards.append(clean_name)
        if normalize_card_name(clean_name) in BANNED_FILTER_ROCKS or normalize_card_name(clean_name) in BANNED_FILTER_LANDS:
            filter_violations.append(clean_name)

        # Count pips
        for pip in re.findall(r'\{([WUBRGC])\}', mana_cost):
            pip_counts[pip] += qty

        front_type = type_line.split("//")[0]
        is_land = "Land" in front_type
        if is_land:
            land_count += qty
        else:
            nonland_count += qty
            nonland_cmc_sum += cmc * qty
            cmc_bucket = min(int(cmc), 7)
            cmc_curve[cmc_bucket] += qty

        rec = {
            "zone": zone,
            "qty": qty,
            "name": clean_name,
            "mana_cost": mana_cost,
            "cmc": cmc,
            "type_line": type_line,
            "oracle_text": oracle_text,
            "pt": pt,
            "game_changer": is_gc,
            "color_identity": ci,
        }
        card_records.append(rec)

        if zone == "COMMANDER":
            type_buckets["Commander"].append(rec)
        elif "Land" in front_type:
            type_buckets["Lands"].append(rec)
        elif "Creature" in front_type:
            type_buckets["Creatures"].append(rec)
        elif "Instant" in front_type:
            type_buckets["Instants"].append(rec)
        elif "Sorcery" in front_type:
            type_buckets["Sorceries"].append(rec)
        elif "Artifact" in front_type:
            type_buckets["Artifacts"].append(rec)
        elif "Enchantment" in front_type:
            type_buckets["Enchantments"].append(rec)
        elif "Planeswalker" in front_type:
            type_buckets["Planeswalkers"].append(rec)
        elif "Battle" in front_type:
            type_buckets["Battles"].append(rec)
        else:
            type_buckets["Other"].append(rec)

    avg_cmc = (nonland_cmc_sum / nonland_count) if nonland_count else 0.0

    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("ELEPHANT-MINNOW MODEL (EMM) — ZERO-CONTEXT BLIND DECK SPECIFICATION")
    lines.append("=" * 80)
    lines.append("NOTICE TO MINNOW SUBAGENT:")
    lines.append("You are receiving ONLY the raw verified 100-card Oracle dossier with zero")
    lines.append("narrative prose or strategy commentary. Do NOT read the deck's .md strategy")
    lines.append("guide during a Cold Comprehension Check. Evaluate strictly what these 100")
    lines.append("cards actually do on the battlefield under the rules of Magic: The Gathering.")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Deck Folder: {deck_dir.name}")
    lines.append(f"Target Bracket: {f'Bracket {target_bracket}' if target_bracket else 'Unspecified'}")
    lines.append(f"Total Cards: {total_cards} (Lands: {land_count} | Nonlands: {nonland_count})")
    lines.append(f"Average Nonland Mana Value (CMC): {avg_cmc:.2f}")
    curve_str = " | ".join(f"{k if k < 7 else '7+'}:{cmc_curve.get(k, 0)}" for k in range(8))
    lines.append(f"Nonland Mana Curve: {curve_str}")
    pip_str = " | ".join(f"{c}:{pip_counts.get(c, 0)}" for c in ["W", "U", "B", "R", "G", "C"] if pip_counts.get(c, 0) > 0)
    lines.append(f"Colored Mana Pips: {pip_str}")
    lines.append(f"WotC Game Changers ({len(game_changers)}): {', '.join(game_changers) if game_changers else 'None'}")
    lines.append(f"Known Mass Land Denial (MLD): {', '.join(mld_cards) if mld_cards else 'None'}")
    lines.append(f"Banned Filter Lands / Filter Signets Present: {', '.join(filter_violations) if filter_violations else 'None'}")
    lines.append("")

    if in_cards or out_cards:
        lines.append("-" * 80)
        lines.append("PROPOSED OVERHAUL DELTA (BLIND SWAP PACKAGE — NO RATIONALE PROVIDED)")
        lines.append("-" * 80)
        if out_cards:
            lines.append("CARDS REMOVED (OUT):")
            for c in out_cards:
                d = lookup_named(c)
                if d:
                    lines.append(f"  - OUT: {d.get('name')} {d.get('mana_cost', '')} — {d.get('type_line', '')} :: {d.get('oracle_text', '').replace(chr(10), ' | ')}")
                else:
                    lines.append(f"  - OUT: {c}")
        if in_cards:
            lines.append("CARDS ADDED (IN):")
            for c in in_cards:
                d = lookup_named(c)
                if d:
                    lines.append(f"  + IN:  {d.get('name')} {d.get('mana_cost', '')} — {d.get('type_line', '')} :: {d.get('oracle_text', '').replace(chr(10), ' | ')}")
                else:
                    lines.append(f"  + IN:  {c}")
        lines.append("")

    bucket_order = [
        "Commander", "Creatures", "Instants", "Sorceries",
        "Artifacts", "Enchantments", "Planeswalkers", "Battles", "Lands", "Other"
    ]
    for bname in bucket_order:
        items = type_buckets.get(bname, [])
        if not items:
            continue
        b_qty = sum(i["qty"] for i in items)
        lines.append("-" * 80)
        lines.append(f"[{bname.upper()} — {b_qty} Cards]")
        lines.append("-" * 80)
        for item in sorted(items, key=lambda x: (x["cmc"], x["name"])):
            gc_tag = " [GAME CHANGER]" if item["game_changer"] else ""
            pt_tag = f" ({item['pt']})" if item["pt"] else ""
            mc_tag = f" {item['mana_cost']}" if item["mana_cost"] else ""
            lines.append(
                f"{item['qty']}x {item['name']}{mc_tag} [CMC {int(item['cmc']) if item['cmc'].is_integer() else item['cmc']}] "
                f"— {item['type_line']}{pt_tag}{gc_tag}"
            )
            if item["oracle_text"]:
                lines.append(f"    Oracle: {item['oracle_text']}")
        lines.append("")

    out_path = deck_dir / "minnow_blind_spec.txt"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def audit_deck_drift(deck_dir: Path) -> Tuple[str, List[str]]:
    """
    Audits a single deck folder for drift across:
    1. moxfield_import.txt
    2. Main .md Plain Text Copy/Paste section (card parity + 2-trailing-space GFM rule)
    3. Main .md Card Explanations bullets (missing or ghost cards)
    4. dti_eval.json card_ledger references
    5. MTG Forge .dck file parity
    """
    divergences: List[str] = []
    mox_path = deck_dir / "moxfield_import.txt"
    md_path = find_main_md_file(deck_dir)

    if not mox_path.exists():
        divergences.append("Missing `moxfield_import.txt`.")
        return deck_dir.name, divergences

    cmdrs, mainboard = parse_moxfield_file(mox_path)
    mox_total = sum(q for q, _ in cmdrs) + sum(q for q, _ in mainboard)
    if mox_total != 100:
        divergences.append(f"`moxfield_import.txt` total card count is **{mox_total}** (expected 100).")

    mox_map: Dict[str, Tuple[int, str]] = {}
    for q, name in cmdrs + mainboard:
        norm = normalize_card_name(name)
        prev_q = mox_map[norm][0] if norm in mox_map else 0
        mox_map[norm] = (prev_q + q, name)

    # Check trailing spaces in moxfield_import.txt
    mox_raw_lines = mox_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    mox_trailing = sum(1 for l in mox_raw_lines if l.endswith("  "))
    if mox_trailing > 0:
        divergences.append(f"`moxfield_import.txt` has {mox_trailing} lines with trailing spaces (should have zero trailing spaces).")

    # Check main .md file
    if not md_path or not md_path.exists():
        divergences.append("Could not locate primary `.md` deck guide file.")
    else:
        md_text = md_path.read_text(encoding="utf-8", errors="ignore")

        # 1. Check Plain Text Copy/Paste section
        pt_match = re.search(
            r'(##\s+[^\n]*Plain Text Copy/Paste[^\n]*\n)(.*?)(?:\n##\s+|\Z)',
            md_text,
            re.DOTALL | re.IGNORECASE,
        )
        if not pt_match:
            divergences.append(f"`{md_path.name}` is missing a `## Plain Text Copy/Paste` section.")
        else:
            pt_body = pt_match.group(2)
            pt_map: Dict[str, int] = defaultdict(int)
            missing_two_spaces = 0
            in_sideboard = False
            for raw_l in pt_body.splitlines():
                stripped = raw_l.strip()
                if not stripped or stripped.startswith("```") or stripped.startswith("["):
                    continue
                hdr = re.sub(r'[^a-z0-9]', '', stripped.lower())
                if hdr in {"sideboard", "maybeboard"}:
                    in_sideboard = True
                    continue
                if hdr in {"commander", "commanders", "deck", "main", "maindeck"}:
                    in_sideboard = False
                    if not raw_l.endswith("  "):
                        missing_two_spaces += 1
                    continue
                if in_sideboard:
                    continue
                m = re.match(r'^(\d+)\s+(.+)$', stripped)
                if m:
                    if not raw_l.endswith("  "):
                        missing_two_spaces += 1
                    q = int(m.group(1))
                    cname = m.group(2).strip()
                    pt_map[normalize_card_name(cname)] += q

            if missing_two_spaces > 0:
                divergences.append(
                    f"`{md_path.name}` Plain Text Copy/Paste has **{missing_two_spaces}** lines missing the required 2 trailing spaces for GFM line breaks."
                )

            if pt_map:
                for norm, (mox_q, orig_name) in mox_map.items():
                    if pt_map.get(norm, 0) != mox_q:
                        divergences.append(
                            f"Plain Text Copy/Paste drift on **{orig_name}**: `moxfield_import.txt` has {mox_q}, `{md_path.name}` Plain Text has {pt_map.get(norm, 0)}."
                        )
                for norm, pt_q in pt_map.items():
                    if norm not in mox_map:
                        divergences.append(
                            f"Plain Text Copy/Paste contains ghost card `{norm}` ({pt_q}x) not present in `moxfield_import.txt`."
                        )

        # 2. Check Card Explanations section for ghost cards or missing explanations
        exp_match = re.search(
            r'(##\s+[^\n]*Card Explanations[^\n]*\n)(.*?)(?:\n##\s+[^\n]*(?:Future Roadmap|Deck Changelog|Plain Text)|\Z)',
            md_text,
            re.DOTALL | re.IGNORECASE,
        )
        if exp_match:
            exp_body = exp_match.group(2)
            explained_cards: Set[str] = set()
            for raw_l in exp_body.splitlines():
                # Match bulleted bold card entries like `* **Sol Ring (1):**` or `- **[Sol Ring](...)**`
                bm = re.match(r'^\s*[\*\-]\s+\*\*(?:\[([^\]]+)\]\([^\)]+\)|([^\*\n:]+?))\*\*[:\s\(]', raw_l)
                if bm:
                    raw_c = (bm.group(1) or bm.group(2) or "").strip()
                    # Strip mana cost in parens or trailing colon
                    raw_c = re.sub(r'\s*\([^\)]*\)\s*$', '', raw_c).rstrip(':').strip()
                    # Handle basic land groupings like "14x Basic Swamp" or "Basic Lands"
                    if not raw_c or "basic" in raw_c.lower():
                        continue
                    raw_c = re.sub(r'^\d+x?\s+', '', raw_c)
                    explained_cards.add(normalize_card_name(raw_c))

            if len(explained_cards) >= 20:
                basics = {"plains", "island", "swamp", "mountain", "forest", "wastes",
                          "snow-covered plains", "snow-covered island", "snow-covered swamp",
                          "snow-covered mountain", "snow-covered forest"}
                cmdr_norms = {normalize_card_name(c) for _, c in cmdrs}
                for norm_c in sorted(explained_cards):
                    if norm_c not in mox_map and norm_c not in basics:
                        divergences.append(
                            f"`{md_path.name}` Card Explanations references ghost card **`{norm_c}`** which is no longer in `moxfield_import.txt`."
                        )
                for norm_c, (_, orig_name) in sorted(mox_map.items()):
                    if norm_c not in explained_cards and norm_c not in basics and norm_c not in cmdr_norms:
                        divergences.append(
                            f"Card **{orig_name}** is in `moxfield_import.txt` but missing from `{md_path.name}` Card Explanations."
                        )

    # 3. Check dti_eval.json ledger for ghost cards
    dti_path = deck_dir / "dti_eval.json"
    if dti_path.exists():
        try:
            dti_data = json.loads(dti_path.read_text(encoding="utf-8"))
            ledger = dti_data.get("card_ledger", {})
            ghost_ledger: Set[str] = set()
            for bench, items in ledger.items():
                if isinstance(items, list):
                    for item in items:
                        cname = item.get("card", "") if isinstance(item, dict) else str(item)
                        if cname and normalize_card_name(cname) not in mox_map:
                            ghost_ledger.add(f"{cname} ({bench.upper()})")
            if ghost_ledger:
                divergences.append(
                    f"`dti_eval.json` card_ledger references ghost cards not in `moxfield_import.txt`: {', '.join(sorted(ghost_ledger))}."
                )
        except Exception as e:
            divergences.append(f"`dti_eval.json` parse error: {e}")

    # 4. Check MTG Forge .dck sync status
    forge_dir = get_default_forge_commander_dir()
    if forge_dir:
        forge_name = determine_forge_deck_name(deck_dir, forge_dir)
        dck_file = forge_dir / f"{forge_name}.dck"
        if not dck_file.exists():
            divergences.append(f"MTG Forge `.dck` file missing at `{dck_file}`.")

    return deck_dir.name, divergences


def render_minnow_reports(deck_dir: Path) -> Tuple[Path, Path]:
    """
    Reads `<deck_dir>/minnow_eval.json` and generates:
      1. `<deck_dir>/minnow_review_report.md`
      2. `<deck_dir>/minnow_report.html`
    """
    eval_path = deck_dir / "minnow_eval.json"
    if not eval_path.exists():
        raise FileNotFoundError(f"Missing {eval_path}. Create minnow_eval.json before running --render.")

    data = json.loads(eval_path.read_text(encoding="utf-8"))
    deck_name = data.get("deck_name", deck_dir.name)
    commander = data.get("commander", "")
    target_bracket = data.get("target_bracket", 3)
    status = data.get("status", "pending_resolution")
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))

    comp = data.get("comprehension_check", {})
    cold_keystone = comp.get("cold_deduced_keystone", "")
    intended_keystone = comp.get("intended_keystone", "")
    cold_shape = comp.get("cold_deduced_shape", "")
    intended_shape = comp.get("intended_shape", "")
    comp_verdict = comp.get("verdict", "PASS")
    comp_notes = comp.get("notes", "")

    findings: List[Dict[str, Any]] = data.get("findings", [])

    # Sort findings by Severity: Blocker -> Major -> Nit
    sev_order = {"blocker": 0, "high": 0, "major": 1, "medium": 1, "nit": 2, "low": 2}
    findings_sorted = sorted(findings, key=lambda f: sev_order.get(str(f.get("severity", "nit")).lower(), 3))

    # 1. Generate Markdown Report (following Google EGM `goldfish_review_report.md` standard)
    md_lines: List[str] = []
    md_lines.append(f"Status: {status}")
    md_lines.append(f"# Minnow Annotated Review Report — {deck_name}")
    md_lines.append("")
    md_lines.append(f"* **Commander:** {commander}")
    md_lines.append(f"* **Target Bracket:** Bracket {target_bracket}")
    md_lines.append(f"* **Date:** {date_str}")
    md_lines.append(f"* **Cold Comprehension Gate:** **{comp_verdict}**")
    md_lines.append("")
    md_lines.append("## 1. Cold Comprehension Check (`emm-comprehension`)")
    md_lines.append("")
    md_lines.append("| Dimension | Cold Minnow Deduction (From 100 Raw Cards Only) | Elephant Intended Design |")
    md_lines.append("| :--- | :--- | :--- |")
    md_lines.append(f"| **3-Step Keystone** | {cold_keystone} | {intended_keystone} |")
    md_lines.append(f"| **Deck Shape & Role** | {cold_shape} | {intended_shape} |")
    md_lines.append("")
    if comp_notes:
        md_lines.append(f"> **Comprehension Analysis:** {comp_notes}")
        md_lines.append("")

    md_lines.append("## 2. Prioritized Findings & Elephant Resolution (`emm-resolve`)")
    md_lines.append("")
    for idx, f in enumerate(findings_sorted, 1):
        title = f.get("title", f"Finding {idx}")
        lens = f.get("lens", "emm-design-critic")
        sev = f.get("severity", "Major")
        scope = f.get("scope", "Main Deck")
        desc = f.get("description", "")
        rationale = f.get("rationale", "")
        suggestion = f.get("elephant_resolution", "PROPOSE FIX")
        justification = f.get("elephant_justification", "")
        proposed_edit = f.get("proposed_edit", "")

        md_lines.append(f"### [Issue {idx}] [`{lens}`] {title} — Severity: {sev}")
        md_lines.append(f"*   **Affected Scope:** {scope}")
        md_lines.append(f"*   **Discrepancy Description:** {desc}")
        md_lines.append(f"*   **Rationale:** {rationale}")
        md_lines.append(f"*   ***Elephant Resolution:*** **{suggestion}**")
        md_lines.append(f"*   ***Justification:*** {justification}")
        if proposed_edit:
            md_lines.append(f"*   ***Proposed Action / Swap:*** {proposed_edit}")
        md_lines.append("")

    md_out = deck_dir / "minnow_review_report.md"
    md_out.write_text("\n".join(md_lines), encoding="utf-8")

    # 2. Generate Interactive HTML Report (`minnow_report.html`)
    blocker_cnt = sum(1 for f in findings_sorted if str(f.get("severity", "")).lower() in {"blocker", "high"})
    major_cnt = sum(1 for f in findings_sorted if str(f.get("severity", "")).lower() in {"major", "medium"})
    nit_cnt = sum(1 for f in findings_sorted if str(f.get("severity", "")).lower() in {"nit", "low"})

    fix_cnt = sum(1 for f in findings_sorted if str(f.get("elephant_resolution", "")).upper() == "PROPOSE FIX")
    contest_cnt = sum(1 for f in findings_sorted if str(f.get("elephant_resolution", "")).upper() == "CONTEST")
    escalate_cnt = sum(1 for f in findings_sorted if str(f.get("elephant_resolution", "")).upper() == "ESCALATE")
    decline_cnt = sum(1 for f in findings_sorted if str(f.get("elephant_resolution", "")).upper() == "DECLINE")

    cards_HTML = []
    for idx, f in enumerate(findings_sorted, 1):
        sev = str(f.get("severity", "Major")).capitalize()
        sev_cls = "sev-blocker" if sev.lower() in {"blocker", "high"} else ("sev-major" if sev.lower() in {"major", "medium"} else "sev-nit")
        res = str(f.get("elephant_resolution", "PROPOSE FIX")).upper()
        res_cls = {
            "PROPOSE FIX": "res-fix",
            "CONTEST": "res-contest",
            "ESCALATE": "res-escalate",
            "DECLINE": "res-decline",
        }.get(res, "res-fix")

        cards_referenced = f.get("cards", [])
        chips_html = ""
        if cards_referenced:
            chip_items = []
            for cname in cards_referenced:
                cdata = lookup_named(cname)
                img_url = ""
                sf_url = f"https://scryfall.com/search?q=!{urllib.parse.quote(f'\"{cname}\"')}"
                if cdata:
                    sf_url = cdata.get("scryfall_uri", sf_url)
                    if cdata.get("image_uris", {}).get("normal"):
                        img_url = cdata["image_uris"]["normal"]
                    elif cdata.get("card_faces") and cdata["card_faces"][0].get("image_uris", {}).get("normal"):
                        img_url = cdata["card_faces"][0]["image_uris"]["normal"]
                chip_items.append(
                    f'<a class="card-chip" href="{html.escape(sf_url)}" target="_blank" data-img="{html.escape(img_url)}">'
                    f'{html.escape(cname)}</a>'
                )
            chips_html = f'<div class="chip-row">{" ".join(chip_items)}</div>'

        cards_HTML.append(f"""
        <div class="finding-card">
          <div class="finding-header">
            <div class="finding-title-group">
              <span class="finding-idx">#{idx}</span>
              <span class="badge {sev_cls}">{html.escape(sev)}</span>
              <span class="badge lens-badge">{html.escape(str(f.get("lens", "emm-critic")))}</span>
              <h3>{html.escape(str(f.get("title", "")))}</h3>
            </div>
            <span class="badge {res_cls}">Elephant: {html.escape(res)}</span>
          </div>
          <div class="finding-scope"><strong>Scope:</strong> {html.escape(str(f.get("scope", "Main Deck")))}</div>
          {chips_html}
          <div class="finding-grid">
            <div class="finding-box minnow-box">
              <div class="box-label">🐟 Minnow Zero-Context Critique</div>
              <p>{html.escape(str(f.get("description", "")))}</p>
              <p class="rationale"><em>Rationale:</em> {html.escape(str(f.get("rationale", "")))}</p>
            </div>
            <div class="finding-box elephant-box">
              <div class="box-label">🐘 Elephant Contextual Arbitration ({html.escape(res)})</div>
              <p>{html.escape(str(f.get("elephant_justification", "")))}</p>
              {f'<p class="proposed-edit"><strong>Proposed Action:</strong> {html.escape(str(f.get("proposed_edit", "")))}</p>' if f.get("proposed_edit") else ''}
            </div>
          </div>
        </div>
        """)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Elephant-Minnow Audit — {html.escape(deck_name)}</title>
<style>
  :root {{
    --bg: #0d1117;
    --panel: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #58a6ff;
    --blocker: #f85149;
    --major: #d29922;
    --nit: #3fb950;
    --fix: #238636;
    --contest: #8957e5;
    --escalate: #da3633;
    --decline: #484f58;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 32px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.55;
  }}
  .container {{ max-width: 1220px; margin: 0 auto; }}
  .hero {{
    background: linear-gradient(135deg, #161b22 0%, #1f2937 100%);
    border: 1px solid var(--border); border-radius: 12px; padding: 24px 28px; margin-bottom: 24px;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;
  }}
  .hero h1 {{ margin: 0 0 6px 0; font-size: 24px; }}
  .hero-sub {{ color: var(--muted); font-size: 14px; }}
  .kpi-row {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin-bottom: 24px;
  }}
  .kpi {{
    background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 16px;
  }}
  .kpi-label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
  .kpi-val {{ font-size: 22px; font-weight: 700; margin-top: 4px; }}
  .section-card {{
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 22px; margin-bottom: 24px;
  }}
  .section-card h2 {{ margin-top: 0; font-size: 18px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }}
  table.comp-table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
  table.comp-table th, table.comp-table td {{
    border: 1px solid var(--border); padding: 12px; text-align: left; vertical-align: top; font-size: 14px;
  }}
  table.comp-table th {{ background: #21262d; color: var(--muted); }}
  .finding-card {{
    background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px;
  }}
  .finding-header {{
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;
  }}
  .finding-title-group {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .finding-title-group h3 {{ margin: 0; font-size: 16px; }}
  .finding-idx {{ color: var(--muted); font-weight: 700; }}
  .badge {{
    padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; display: inline-block;
  }}
  .sev-blocker {{ background: rgba(248,81,73,0.18); color: #ff7b72; border: 1px solid var(--blocker); }}
  .sev-major {{ background: rgba(210,153,34,0.18); color: #e3b341; border: 1px solid var(--major); }}
  .sev-nit {{ background: rgba(63,185,80,0.18); color: #56d364; border: 1px solid var(--nit); }}
  .lens-badge {{ background: #21262d; color: var(--accent); border: 1px solid var(--border); font-family: monospace; }}
  .res-fix {{ background: rgba(35,134,54,0.22); color: #56d364; border: 1px solid var(--fix); }}
  .res-contest {{ background: rgba(137,87,229,0.22); color: #d2a8ff; border: 1px solid var(--contest); }}
  .res-escalate {{ background: rgba(218,54,51,0.22); color: #ffa198; border: 1px solid var(--escalate); }}
  .res-decline {{ background: rgba(72,79,88,0.25); color: var(--muted); border: 1px solid var(--decline); }}
  .finding-scope {{ font-size: 13px; color: var(--muted); margin-bottom: 10px; }}
  .chip-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
  .card-chip {{
    background: #21262d; color: var(--accent); border: 1px solid var(--border);
    padding: 3px 10px; border-radius: 6px; font-size: 12px; text-decoration: none;
  }}
  .card-chip:hover {{ border-color: var(--accent); }}
  .finding-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  @media (max-width: 820px) {{ .finding-grid {{ grid-template-columns: 1fr; }} }}
  .finding-box {{
    background: #0d1117; border: 1px solid var(--border); border-radius: 8px; padding: 14px; font-size: 14px;
  }}
  .box-label {{ font-weight: 700; font-size: 12px; text-transform: uppercase; margin-bottom: 8px; color: var(--muted); }}
  .rationale {{ color: var(--muted); font-size: 13px; margin-bottom: 0; }}
  .proposed-edit {{
    background: rgba(56,139,253,0.1); border-left: 3px solid var(--accent); padding: 8px 10px; margin-bottom: 0; border-radius: 4px;
  }}
  #hover-preview {{
    position: fixed; pointer-events: none; display: none; z-index: 9999;
    width: 240px; border-radius: 12px; box-shadow: 0 12px 32px rgba(0,0,0,0.85);
  }}
</style>
</head>
<body>
<div class="container">
  <div class="hero">
    <div>
      <h1>🐘🐟 Elephant-Minnow Audit — {html.escape(deck_name)}</h1>
      <div class="hero-sub">Commander: <strong>{html.escape(commander)}</strong> &bull; Target: <strong>Bracket {target_bracket}</strong> &bull; Date: {html.escape(date_str)}</div>
    </div>
    <div>
      <span class="badge {'sev-nit' if comp_verdict.upper() == 'PASS' else 'sev-major'}">Comprehension Gate: {html.escape(comp_verdict)}</span>
      <span class="badge lens-badge">Status: {html.escape(status)}</span>
    </div>
  </div>

  <div class="kpi-row">
    <div class="kpi">
      <div class="kpi-label">Minnow Findings</div>
      <div class="kpi-val">{len(findings_sorted)} Total</div>
      <div class="hero-sub">🔴 {blocker_cnt} Blocker &bull; 🟡 {major_cnt} Major &bull; 🟢 {nit_cnt} Nit</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Propose Fix</div>
      <div class="kpi-val" style="color:#56d364">{fix_cnt}</div>
      <div class="hero-sub">Valid critiques queued for swap/edit</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Contested</div>
      <div class="kpi-val" style="color:#d2a8ff">{contest_cnt}</div>
      <div class="hero-sub">Defended with checkable evidence</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Escalated / Declined</div>
      <div class="kpi-val" style="color:#ffa198">{escalate_cnt} / {decline_cnt}</div>
      <div class="hero-sub">Owner arbitration / Nits</div>
    </div>
  </div>

  <div class="section-card">
    <h2>1. Cold Comprehension Check (Information Firewall Test)</h2>
    <p style="color:var(--muted);font-size:14px;margin-top:0;">
      A stateless Minnow received <strong>only</strong> the 100 raw cards in <code>minnow_blind_spec.txt</code> (zero strategy prose) and was required to deduce the deck's Keystone and Geometric Shape cold.
    </p>
    <table class="comp-table">
      <thead>
        <tr>
          <th style="width:18%">Dimension</th>
          <th style="width:41%">🐟 Cold Minnow Deduction (Raw 100 Cards Only)</th>
          <th style="width:41%">🐘 Elephant Intended Design</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>3-Step Keystone</strong></td>
          <td>{html.escape(cold_keystone)}</td>
          <td>{html.escape(intended_keystone)}</td>
        </tr>
        <tr>
          <td><strong>Deck Shape &amp; Role</strong></td>
          <td>{html.escape(cold_shape)}</td>
          <td>{html.escape(intended_shape)}</td>
        </tr>
      </tbody>
    </table>
    {f'<p style="margin:12px 0 0 0;font-size:14px;"><strong>Diagnostic Note:</strong> {html.escape(comp_notes)}</p>' if comp_notes else ''}
  </div>

  <h2 style="font-size:18px;margin-bottom:14px;">2. Prioritized Minnow Findings &amp; Elephant Arbitration</h2>
  {"".join(cards_HTML)}
</div>
<img id="hover-preview" src="" alt="Card preview" />
<script>
  const preview = document.getElementById('hover-preview');
  document.querySelectorAll('.card-chip').forEach(chip => {{
    chip.addEventListener('mouseenter', e => {{
      const img = chip.getAttribute('data-img');
      if (img) {{ preview.src = img; preview.style.display = 'block'; }}
    }});
    chip.addEventListener('mousemove', e => {{
      preview.style.left = Math.min(e.clientX + 18, window.innerWidth - 260) + 'px';
      preview.style.top = Math.min(e.clientY - 40, window.innerHeight - 360) + 'px';
    }});
    chip.addEventListener('mouseleave', () => {{ preview.style.display = 'none'; }});
  }});
</script>
</body>
</html>
"""
    html_out = deck_dir / "minnow_report.html"
    html_out.write_text(html_doc, encoding="utf-8")
    return md_out, html_out


def main():
    parser = argparse.ArgumentParser(description="Elephant-Minnow Model (EMM) Blind Spec, Drift & Report Tool")
    parser.add_argument("deck_path", nargs="?", default=None, help="Path to deck folder")
    parser.add_argument("--pack", action="store_true", help="Generate prose-free minnow_blind_spec.txt for zero-context Minnow review")
    parser.add_argument("--drift", action="store_true", help="Run emm-drift-report on deck folder (or --all)")
    parser.add_argument("--render", action="store_true", help="Render minnow_eval.json into minnow_review_report.md and minnow_report.html")
    parser.add_argument("--all", action="store_true", help="Run --drift across all Owned and Planning Commander decks")
    parser.add_argument("--bracket", type=int, default=None, help="Explicit target Bracket (1-5) for --pack")
    parser.add_argument("--in", dest="in_cards", nargs="*", default=None, help="Candidate IN cards for blind swap spec")
    parser.add_argument("--out", dest="out_cards", nargs="*", default=None, help="Candidate OUT cards for blind swap spec")

    args = parser.parse_args()

    if args.drift and args.all:
        base = REPO_ROOT / "commander_decks"
        folders = []
        for sub in ["Owned", "Planning"]:
            subdir = base / sub
            if subdir.exists():
                for d in sorted(subdir.iterdir()):
                    if d.is_dir() and (d / "moxfield_import.txt").exists():
                        folders.append(d)
        report_lines = [f"# Repository-Wide EMM Drift Report ({datetime.now().strftime('%Y-%m-%d')})", ""]
        drift_count = 0
        for d in folders:
            name, divs = audit_deck_drift(d)
            rel = d.relative_to(REPO_ROOT)
            report_lines.append(f"## {name} (`{rel}`)")
            if divs:
                drift_count += 1
                for item in divs:
                    report_lines.append(f"- {item}")
                print(f"[DRIFT] {rel}: {len(divs)} issue(s)")
            else:
                report_lines.append("No drift detected.")
                print(f"[OK]    {rel}: No drift detected.")
            report_lines.append("")
        print(f"\n[EMM Drift Summary] {len(folders) - drift_count}/{len(folders)} decks clean, {drift_count} with drift.")
        return

    if not args.deck_path:
        parser.print_help()
        sys.exit(1)

    target = Path(args.deck_path).resolve()
    deck_dir = target.parent if target.is_file() else target

    if args.pack:
        out_path = pack_blind_spec(
            deck_dir,
            in_cards=args.in_cards,
            out_cards=args.out_cards,
            target_bracket=args.bracket,
        )
        print(f"[EMM Pack] Wrote blind specification to: {out_path}")

    if args.drift:
        name, divs = audit_deck_drift(deck_dir)
        print(f"## {name}")
        if not divs:
            print("No drift detected.")
        else:
            for d in divs:
                print(f"- {d}")

    if args.render:
        md_out, html_out = render_minnow_reports(deck_dir)
        print(f"[EMM Render] Wrote Markdown report: {md_out}")
        print(f"[EMM Render] Wrote HTML dashboard:  {html_out}")


if __name__ == "__main__":
    main()
