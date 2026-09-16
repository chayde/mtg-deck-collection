#!/usr/bin/env python3
"""
scripts/swap_matrix.py — Visual Swap Matrix & Mechanics Pre-Check Utility

Analyzes proposed Commander deck card swaps with Scryfall data, verifies Bracket
and Game Changer compliance, performs mathematical deltas (CMC, curve, pips, types, price),
audits rules mechanics (CR 302.6 summoning sickness, tapland tempo, permanent ban checks),
generates an interactive visual HTML matrix with 240px card art, and atomically
applies the Triple-Update Rule across markdown deck files, plain text sections,
and moxfield_import.txt.

Usage:
  python scripts/swap_matrix.py <deck_path> --in "Card A" "Card B" --out "Card C" "Card D" [options]

Examples:
  # Dry-run analysis with visual HTML generation:
  python scripts/swap_matrix.py "commander_decks/Planning/UltronArtificialMalevolence/moxfield_import.txt" \\
      --in "Arc Reactor" "Panharmonicon" \\
      --out "The Endstone" "Banner of Kinship" \\
      --reason "Lower curve and double ETB copy triggers"

  # Atomic apply (executes Triple-Update on .md, plain text, and moxfield_import.txt):
  python scripts/swap_matrix.py "commander_decks/Planning/UltronArtificialMalevolence/moxfield_import.txt" \\
      --in "Arc Reactor" "Panharmonicon" \\
      --out "The Endstone" "Banner of Kinship" \\
      --reason "Lower curve and double ETB copy triggers" \\
      --apply
"""

import os
import sys
import re
import time
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

# Ensure scripts/ directory is in python path to import scryfall_lookup
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from scryfall_lookup import lookup_named
except ImportError:
    print("Error: Could not import lookup_named from scryfall_lookup.py", file=sys.stderr)
    sys.exit(1)

# --- Codified Preferences & Ban Lists ---
FILTER_LANDS = {
    "shadowblood ridge", "desolate mire", "darkwater catacombs", "mossfire valley",
    "sungrass prairie", "cascade bluffs", "fetid heath", "fire-lit thicket",
    "flooded grove", "graven cairns", "mystic gate", "rugged prairie",
    "sunken ruins", "twilight mire", "wooded bastion"
}

FILTER_ROCKS = {
    "azorius signet", "boros signet", "dimir signet", "golgari signet",
    "gruul signet", "izzet signet", "orzhov signet", "rakdos signet",
    "selesnya signet", "simic signet"
}

HASTE_ENABLERS = {
    "thousand-year elixir", "lightning greaves", "swiftfoot boots", "crashing drawbridge",
    "anger", "concordant crossroads", "mass hysteria", "urabrask the hidden",
    "fervor", "hammer of purphoros", "rising of the day", "tuk-tuk rubblefort",
    "rhythm of the wild", "fires of yavimaya", "tyvar, jubilant brawler", "boots of speed"
}

EXILE_REPLACEMENT_EFFECTS = {
    "rest in peace", "dauthi voidwalker", "leyline of the void", "planar void",
    "samurai of the pale curtain", "drana and linvala", "kalitas, traitor of ghet"
}

BASIC_LANDS = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes",
               "Snow-Covered Plains", "Snow-Covered Island", "Snow-Covered Swamp",
               "Snow-Covered Mountain", "Snow-Covered Forest", "Snow-Covered Wastes"}


def clean_card_name(raw: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Parses input string like:
      - 'Arc Reactor'
      - 'Arc Reactor: Improvise rock'
      - 'Arc Reactor | Mana Acceleration & Rocks | Improvise rock'
    Returns: (card_name, category_override, rationale)
    """
    raw = raw.strip()
    category = None
    rationale = None

    if "|" in raw:
        parts = [p.strip() for p in raw.split("|")]
        name = parts[0]
        if len(parts) >= 2 and parts[1]:
            category = parts[1]
        if len(parts) >= 3 and parts[2]:
            rationale = parts[2]
        return name, category, rationale
    elif ":" in raw:
        parts = [p.strip() for p in raw.split(":", 1)]
        name = parts[0]
        rationale = parts[1] if len(parts) > 1 else None
        return name, category, rationale
    return raw, category, rationale


def get_card_info(name: str) -> Dict[str, Any]:
    """Fetches card data via scryfall_lookup and normalizes essential attributes."""
    data = lookup_named(name)
    if not data:
        # Fallback dictionary if lookup fails
        return {
            "name": name,
            "mana_cost": "",
            "cmc": 0,
            "type_line": "Unknown",
            "oracle_text": "",
            "colors": [],
            "color_identity": [],
            "game_changer": False,
            "usd": "0.00",
            "scryfall_uri": f"https://scryfall.com/search?q=!\"{name}\"",
            "image_uri": "https://cards.scryfall.io/back.jpg",
            "is_land": False,
            "is_creature": False,
            "is_artifact": False,
            "is_enchantment": False,
            "is_instant": False,
            "is_sorcery": False,
            "is_planeswalker": False
        }

    # Extract image URI (supporting standard and DFC front faces)
    img = None
    if "image_uris" in data and data["image_uris"].get("normal"):
        img = data["image_uris"]["normal"]
    elif "card_faces" in data and len(data["card_faces"]) > 0 and data["card_faces"][0].get("image_uris", {}).get("normal"):
        img = data["card_faces"][0]["image_uris"]["normal"]

    # Extract mana cost and oracle text
    mana_cost = data.get("mana_cost", "")
    oracle = data.get("oracle_text", "")
    type_line = data.get("type_line", "")

    if not mana_cost and "card_faces" in data and len(data["card_faces"]) > 0:
        mana_cost = data["card_faces"][0].get("mana_cost", "")
        if not oracle:
            oracle = "\n//\n".join([f.get("oracle_text", "") for f in data["card_faces"]])

    prices = data.get("prices", {})
    usd_str = prices.get("usd") or prices.get("usd_foil") or "0.00"

    is_land = "Land" in type_line
    is_creature = "Creature" in type_line
    is_artifact = "Artifact" in type_line
    is_enchantment = "Enchantment" in type_line
    is_instant = "Instant" in type_line
    is_sorcery = "Sorcery" in type_line
    is_planeswalker = "Planeswalker" in type_line

    return {
        "name": data.get("name", name),
        "mana_cost": mana_cost,
        "cmc": int(data.get("cmc", 0)),
        "type_line": type_line,
        "oracle_text": oracle,
        "colors": data.get("colors", []),
        "color_identity": data.get("color_identity", []),
        "game_changer": bool(data.get("game_changer", False)),
        "usd": usd_str,
        "scryfall_uri": data.get("scryfall_uri", f"https://scryfall.com/search?q=!\"{name}\""),
        "image_uri": img or "https://cards.scryfall.io/back.jpg",
        "is_land": is_land,
        "is_creature": is_creature,
        "is_artifact": is_artifact,
        "is_enchantment": is_enchantment,
        "is_instant": is_instant,
        "is_sorcery": is_sorcery,
        "is_planeswalker": is_planeswalker
    }


def find_deck_files(target_path: str) -> Tuple[Optional[Path], Optional[Path], Path]:
    """
    Resolves target path to (moxfield_path, md_path, deck_dir).
    Supports pointing to moxfield_import.txt, deck.md, or the deck directory.
    """
    p = Path(target_path).resolve()
    if p.is_dir():
        deck_dir = p
        moxfield = deck_dir / "moxfield_import.txt"
        md_files = [f for f in deck_dir.glob("*.md") if f.name not in {"order_tracking.md", "GOLDFISH_LOG.md", "README.md"}]
        md_path = md_files[0] if md_files else None
        return moxfield if moxfield.exists() else None, md_path, deck_dir

    deck_dir = p.parent
    if p.name == "moxfield_import.txt":
        moxfield = p
        md_files = [f for f in deck_dir.glob("*.md") if f.name not in {"order_tracking.md", "GOLDFISH_LOG.md", "README.md"}]
        md_path = md_files[0] if md_files else None
        return moxfield, md_path, deck_dir

    if p.suffix == ".md":
        md_path = p
        moxfield = deck_dir / "moxfield_import.txt"
        return moxfield if moxfield.exists() else None, md_path, deck_dir

    return None, None, deck_dir


def parse_moxfield_list(file_path: Path) -> Tuple[Optional[str], List[str]]:
    """Parses commander and deck list from moxfield_import.txt or similar text."""
    if not file_path or not file_path.exists():
        return None, []

    content = file_path.read_text(encoding="utf-8")
    cm = re.search(r'(?:COMMANDER|Commander):?\s*(.*?)(?=\n\n|\n[A-Za-z]+:|\Z)', content, re.DOTALL)
    commander = None
    if cm:
        for line in cm.group(1).strip().splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^\d+\s+(.+)', line)
            commander = m.group(1).strip() if m else line
            break

    dm = re.search(r'(?:DECK|Deck|MAIN DECK|Main Deck):?\s*(.*?)(?=\n\n|\n[A-Za-z]+:|\Z)', content, re.DOTALL)
    cards = []
    if dm:
        for line in dm.group(1).strip().splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^(\d+)\s+(.+)', line)
            if m:
                count = int(m.group(1))
                name = m.group(2).strip()
                cards.extend([name] * count)
            else:
                cards.append(line)
    return commander, cards


def detect_deck_bracket(md_path: Optional[Path], default_bracket: int = 3) -> int:
    """Extracts target bracket from markdown file metadata or body."""
    if not md_path or not md_path.exists():
        return default_bracket
    content = md_path.read_text(encoding="utf-8")
    m = re.search(r'\*?\s*\*\*Bracket:\*\*\s*(\d)', content, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return default_bracket


def extract_pips(mana_cost: str) -> Dict[str, int]:
    """Counts colored mana pips in a mana cost string."""
    pips = {}
    for sym in re.findall(r'\{([WUBRGC])\}', mana_cost):
        pips[sym] = pips.get(sym, 0) + 1
    return pips


def calculate_metrics(cards_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Computes deck metrics: avg CMC, curve histogram, pips, types, price, game changers."""
    nonland_spells = [c for c in cards_data if not c["is_land"]]
    total_nonland = len(nonland_spells)

    avg_cmc = (sum(c["cmc"] for c in nonland_spells) / total_nonland) if total_nonland else 0.0

    curve = { "0-1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6+": 0 }
    for c in nonland_spells:
        cmc = c["cmc"]
        if cmc <= 1:
            curve["0-1"] += 1
        elif cmc == 2:
            curve["2"] += 1
        elif cmc == 3:
            curve["3"] += 1
        elif cmc == 4:
            curve["4"] += 1
        elif cmc == 5:
            curve["5"] += 1
        else:
            curve["6+"] += 1

    pips = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0, "C": 0}
    for c in nonland_spells:
        for k, v in extract_pips(c["mana_cost"]).items():
            if k in pips:
                pips[k] += v

    types = {
        "Creature": sum(1 for c in cards_data if c["is_creature"]),
        "Artifact": sum(1 for c in cards_data if c["is_artifact"]),
        "Enchantment": sum(1 for c in cards_data if c["is_enchantment"]),
        "Instant": sum(1 for c in cards_data if c["is_instant"]),
        "Sorcery": sum(1 for c in cards_data if c["is_sorcery"]),
        "Planeswalker": sum(1 for c in cards_data if c["is_planeswalker"]),
        "Land": sum(1 for c in cards_data if c["is_land"]),
    }

    game_changers = [c["name"] for c in cards_data if c["game_changer"]]

    total_price = 0.0
    for c in cards_data:
        try:
            total_price += float(c["usd"])
        except ValueError:
            pass

    return {
        "count": len(cards_data),
        "nonland_count": total_nonland,
        "avg_cmc": avg_cmc,
        "curve": curve,
        "pips": pips,
        "types": types,
        "game_changers": game_changers,
        "total_price": total_price
    }


def audit_rules(deck_data: List[Dict[str, Any]],
                in_cards_data: List[Dict[str, Any]],
                commander_data: Optional[Dict[str, Any]],
                bracket: int) -> List[Dict[str, str]]:
    """
    Audits incoming cards against rules mechanics:
      - Color identity violations
      - Filter lands / Filter rocks ban (GEMINI.md)
      - CR 302.6 Summoning sickness for animated tap permanents
      - Tapland tempo drag
      - Dies triggers vs exile replacement
    """
    notes = []
    deck_names_lower = {c["name"].lower() for c in deck_data}
    has_haste_enabler = any(c in deck_names_lower for c in HASTE_ENABLERS)
    has_exile_replacement = any(c in deck_names_lower for c in EXILE_REPLACEMENT_EFFECTS)

    cmd_ci = set(commander_data.get("color_identity", [])) if commander_data else set()

    for c in in_cards_data:
        name_lower = c["name"].lower()
        oracle_lower = c["oracle_text"].lower()

        # 1. Color identity
        card_ci = set(c["color_identity"])
        if not card_ci.issubset(cmd_ci):
            diff = card_ci - cmd_ci
            notes.append({
                "severity": "CRITICAL",
                "card": c["name"],
                "category": "Color Identity Violation",
                "message": f"Contains off-identity colors ({', '.join(diff)}) not allowed by commander identity ({', '.join(cmd_ci) or 'Colorless'})."
            })

        # 2. Filter land ban
        if name_lower in FILTER_LANDS:
            notes.append({
                "severity": "WARNING",
                "card": c["name"],
                "category": "User Preference Ban",
                "message": "Filter land prohibited by permanent project rule in GEMINI.md."
            })

        # 3. Filter rock ban
        if name_lower in FILTER_ROCKS:
            notes.append({
                "severity": "WARNING",
                "card": c["name"],
                "category": "User Preference Ban",
                "message": "Filter mana rock (Signet) prohibited by permanent project rule in GEMINI.md."
            })

        # 4. CR 302.6 Summoning sickness on tap abilities
        has_tap_ability = "{t}" in oracle_lower or "{t}:" in oracle_lower
        is_or_creates_creature = (c["is_creature"] or "becomes a creature" in oracle_lower or
                                  "token that's a copy" in oracle_lower or "robot villain" in oracle_lower)
        if has_tap_ability and is_or_creates_creature and not has_haste_enabler:
            notes.append({
                "severity": "INFO",
                "card": c["name"],
                "category": "Mechanics (CR 302.6)",
                "message": "Activated {T} ability requires haste to use on the turn it enters while a creature."
            })

        # 5. Tapland tempo drag
        if c["is_land"] and "enters tapped" in oracle_lower:
            # Check for crowd-land exception
            if "two or more opponents" not in oracle_lower and "unless" not in oracle_lower:
                notes.append({
                    "severity": "INFO",
                    "card": c["name"],
                    "category": "Tempo Drag",
                    "message": "Enters the battlefield tapped unconditionally."
                })

        # 6. Dies trigger vs exile replacement
        if ("when this creature dies" in oracle_lower or "whenever a creature dies" in oracle_lower) and has_exile_replacement:
            notes.append({
                "severity": "INFO",
                "card": c["name"],
                "category": "Synergy Clash",
                "message": "Deck runs graveyard exile effects (e.g. Rest in Peace/Dauthi) which prevent death triggers."
            })

    return notes


def generate_html_matrix(output_path: Path,
                         deck_name: str,
                         commander_name: str,
                         bracket: int,
                         swaps: List[Dict[str, Any]],
                         pre_metrics: Dict[str, Any],
                         post_metrics: Dict[str, Any],
                         rules_notes: List[Dict[str, str]],
                         reason: str) -> None:
    """Generates a responsive, standalone visual HTML swap report with 240px card art."""
    cmc_diff = post_metrics["avg_cmc"] - pre_metrics["avg_cmc"]
    cmc_sign = "+" if cmc_diff > 0 else ""
    cmc_class = "negative" if cmc_diff > 0.1 else ("positive" if cmc_diff < -0.1 else "neutral")

    gc_pre_cnt = len(pre_metrics["game_changers"])
    gc_post_cnt = len(post_metrics["game_changers"])
    gc_status = "PASS" if (bracket > 3 or gc_post_cnt <= 3) else "EXCEEDED"
    gc_class = "positive" if gc_status == "PASS" else "critical"

    price_diff = post_metrics["total_price"] - pre_metrics["total_price"]
    price_sign = "+" if price_diff > 0 else ""

    # Build Swap Cards HTML
    swap_cards_html = []
    for i, s in enumerate(swaps, start=1):
        out_card = s["out"]
        in_card = s["in"]
        swap_cards_html.append(f"""
        <div class="swap-row">
            <div class="card-column out-col">
                <div class="col-header badge-out">OUT #{i} — CUT</div>
                <div class="card-card">
                    <div class="img-wrap">
                        <img src="{out_card['image_uri']}" alt="{out_card['name']}" loading="lazy" />
                    </div>
                    <div class="card-info">
                        <div class="card-title">
                            <a href="{out_card['scryfall_uri']}" target="_blank">{out_card['name']}</a>
                            <span class="mana-cost">{out_card['mana_cost']}</span>
                        </div>
                        <div class="type-line">{out_card['type_line']} — CMC {out_card['cmc']}</div>
                        <div class="oracle-box">{out_card['oracle_text'].replace(chr(10), '<br>')}</div>
                    </div>
                </div>
            </div>

            <div class="swap-arrow">➔</div>

            <div class="card-column in-col">
                <div class="col-header badge-in">IN #{i} — ADD</div>
                <div class="card-card">
                    <div class="img-wrap">
                        <img src="{in_card['image_uri']}" alt="{in_card['name']}" loading="lazy" />
                    </div>
                    <div class="card-info">
                        <div class="card-title">
                            <a href="{in_card['scryfall_uri']}" target="_blank">{in_card['name']}</a>
                            <span class="mana-cost">{in_card['mana_cost']}</span>
                        </div>
                        <div class="type-line">{in_card['type_line']} — CMC {in_card['cmc']}</div>
                        <div class="oracle-box">{in_card['oracle_text'].replace(chr(10), '<br>')}</div>
                        {f'<div class="rationale-tag"><strong>Role / Reason:</strong> {s["rationale"]}</div>' if s.get("rationale") else ''}
                    </div>
                </div>
            </div>
        </div>
        """)

    # Build Rules Notes HTML
    rules_html = []
    if rules_notes:
        for r in rules_notes:
            sev_class = r["severity"].lower()
            rules_html.append(f"""
            <div class="rule-item {sev_class}">
                <span class="rule-badge {sev_class}">{r['severity']}</span>
                <strong>{r['card']}:</strong> [{r['category']}] {r['message']}
            </div>
            """)
    else:
        rules_html.append("<div class='rule-item positive'>All clear! No rules traps or preference violations detected.</div>")

    # Curve bar charts
    curve_bars = []
    max_curve_val = max(max(pre_metrics["curve"].values()), max(post_metrics["curve"].values()), 1)
    for bucket in ["0-1", "2", "3", "4", "5", "6+"]:
        pre_val = pre_metrics["curve"][bucket]
        post_val = post_metrics["curve"][bucket]
        pre_pct = int(pre_val / max_curve_val * 100)
        post_pct = int(post_val / max_curve_val * 100)
        curve_bars.append(f"""
        <div class="curve-col">
            <div class="curve-bars-pair">
                <div class="bar bar-pre" style="height: {pre_pct}%;" title="Pre: {pre_val}"></div>
                <div class="bar bar-post" style="height: {post_pct}%;" title="Post: {post_val}"></div>
            </div>
            <div class="curve-label">{bucket}</div>
            <div class="curve-counts">{pre_val}➔{post_val}</div>
        </div>
        """)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Swap Matrix: {deck_name}</title>
<style>
  :root {{
    --bg-main: #0d1117;
    --bg-card: #161b22;
    --border-color: #30363d;
    --text-main: #c9d1d9;
    --text-muted: #8b949e;
    --out-red: #f85149;
    --out-bg: rgba(248, 81, 73, 0.1);
    --in-green: #3fb950;
    --in-bg: rgba(63, 185, 80, 0.1);
    --gold: #d29922;
    --blue: #58a6ff;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: var(--bg-main);
    color: var(--text-main);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    padding: 24px;
    line-height: 1.5;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  header {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
  }}
  h1 {{ font-size: 24px; color: #fff; margin-bottom: 8px; }}
  .sub-header {{ color: var(--text-muted); font-size: 14px; margin-bottom: 16px; }}
  
  /* Delta Dashboard Grid */
  .dashboard-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-top: 16px;
  }}
  .metric-card {{
    background: #21262d;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 14px;
  }}
  .metric-title {{ font-size: 12px; text-transform: uppercase; color: var(--text-muted); font-weight: 600; }}
  .metric-value {{ font-size: 20px; font-weight: bold; margin: 4px 0; }}
  .metric-sub {{ font-size: 12px; }}
  
  .positive {{ color: var(--in-green); }}
  .negative {{ color: var(--out-red); }}
  .critical {{ color: var(--out-red); font-weight: bold; }}
  .neutral {{ color: var(--text-muted); }}

  /* Curve Section */
  .curve-section {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
  }}
  .curve-chart {{
    display: flex;
    align-items: flex-end;
    gap: 20px;
    height: 140px;
    padding-top: 20px;
    border-bottom: 1px solid var(--border-color);
  }}
  .curve-col {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
  }}
  .curve-bars-pair {{
    display: flex;
    align-items: flex-end;
    gap: 4px;
    width: 36px;
    height: 100px;
  }}
  .bar {{ width: 16px; border-radius: 3px 3px 0 0; }}
  .bar-pre {{ background: #8b949e; opacity: 0.6; }}
  .bar-post {{ background: var(--blue); }}
  .curve-label {{ font-size: 12px; font-weight: 600; margin-top: 6px; }}
  .curve-counts {{ font-size: 10px; color: var(--text-muted); }}

  /* Rules Watchdog */
  .rules-section {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 24px;
  }}
  .rules-title {{ font-size: 16px; font-weight: bold; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
  .rule-item {{
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 13px;
    border: 1px solid transparent;
  }}
  .rule-item.critical {{ background: rgba(248, 81, 73, 0.15); border-color: var(--out-red); }}
  .rule-item.warning {{ background: rgba(210, 153, 34, 0.15); border-color: var(--gold); }}
  .rule-item.info {{ background: rgba(88, 166, 255, 0.1); border-color: var(--blue); }}
  .rule-badge {{
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    margin-right: 6px;
  }}
  .rule-badge.critical {{ background: var(--out-red); color: #fff; }}
  .rule-badge.warning {{ background: var(--gold); color: #000; }}
  .rule-badge.info {{ background: var(--blue); color: #000; }}

  /* Swap Rows */
  .swap-row {{
    display: flex;
    align-items: stretch;
    gap: 16px;
    margin-bottom: 20px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
  }}
  .card-column {{ flex: 1; display: flex; flex-direction: column; }}
  .col-header {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 4px 8px;
    border-radius: 4px;
    margin-bottom: 12px;
    display: inline-block;
    align-self: flex-start;
  }}
  .badge-out {{ background: var(--out-bg); color: var(--out-red); border: 1px solid var(--out-red); }}
  .badge-in {{ background: var(--in-bg); color: var(--in-green); border: 1px solid var(--in-green); }}
  
  .card-card {{
    display: flex;
    gap: 16px;
    flex: 1;
  }}
  .img-wrap {{
    width: 140px;
    flex-shrink: 0;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    transition: transform 0.2s ease;
  }}
  .img-wrap:hover {{
    transform: scale(1.08);
    z-index: 10;
  }}
  .img-wrap img {{ width: 100%; display: block; border-radius: 6px; }}
  .card-info {{ flex: 1; }}
  .card-title {{
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .card-title a {{ color: #fff; text-decoration: none; }}
  .card-title a:hover {{ text-decoration: underline; color: var(--blue); }}
  .mana-cost {{ font-family: monospace; font-size: 14px; color: var(--gold); }}
  .type-line {{ font-size: 12px; color: var(--text-muted); margin-bottom: 8px; }}
  .oracle-box {{
    background: #0d1117;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 8px 10px;
    font-size: 12px;
    color: #e6edf3;
    max-height: 110px;
    overflow-y: auto;
  }}
  .rationale-tag {{
    margin-top: 8px;
    font-size: 12px;
    background: rgba(88, 166, 255, 0.1);
    border-left: 3px solid var(--blue);
    padding: 6px 8px;
    border-radius: 0 4px 4px 0;
  }}
  .swap-arrow {{
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: var(--text-muted);
    padding: 0 8px;
  }}

  @media (max-width: 850px) {{
    .swap-row {{ flex-direction: column; }}
    .swap-arrow {{ transform: rotate(90deg); margin: 8px 0; }}
    .card-card {{ flex-direction: column; }}
    .img-wrap {{ width: 180px; margin: 0 auto; }}
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Visual Swap Matrix — {deck_name}</h1>
    <div class="sub-header">
      Commander: <strong>{commander_name}</strong> | Target Bracket: <strong>Bracket {bracket}</strong> | 
      Generated: <strong>{time.strftime('%Y-%m-%d %H:%M:%S')}</strong>
    </div>
    <div class="rationale-tag"><strong>Proposal Logic:</strong> {reason}</div>

    <div class="dashboard-grid">
      <div class="metric-card">
        <div class="metric-title">Average CMC (Nonland)</div>
        <div class="metric-value {cmc_class}">{pre_metrics['avg_cmc']:.2f} ➔ {post_metrics['avg_cmc']:.2f}</div>
        <div class="metric-sub">Delta: {cmc_sign}{cmc_diff:.2f}</div>
      </div>
      <div class="metric-card">
        <div class="metric-title">Game Changers (Bracket {bracket})</div>
        <div class="metric-value {gc_class}">{gc_post_cnt} / 3</div>
        <div class="metric-sub">Status: {gc_status} (Pre: {gc_pre_cnt})</div>
      </div>
      <div class="metric-card">
        <div class="metric-title">Deck Size & Balance</div>
        <div class="metric-value">{post_metrics['count']} Cards</div>
        <div class="metric-sub">Creatures: {pre_metrics['types']['Creature']}➔{post_metrics['types']['Creature']} | Lands: {post_metrics['types']['Land']}</div>
      </div>
      <div class="metric-card">
        <div class="metric-title">Est. Market Value Impact</div>
        <div class="metric-value">${post_metrics['total_price']:.2f}</div>
        <div class="metric-sub">Delta: {price_sign}${price_diff:.2f}</div>
      </div>
    </div>
  </header>

  <div class="rules-section">
    <div class="rules-title">🛡️ Rules & Synergy Watchdog</div>
    {''.join(rules_html)}
  </div>

  <div class="curve-section">
    <div class="rules-title">📊 Mana Curve Shift (Grey = Pre, Blue = Post)</div>
    <div class="curve-chart">
      {''.join(curve_bars)}
    </div>
  </div>

  <div class="swaps-container">
    {''.join(swap_cards_html)}
  </div>
</div>
</body>
</html>
"""
    output_path.write_text(html_content, encoding="utf-8")
    print(f"[matrix] Standalone visual HTML generated at: {output_path}")


def apply_triple_update(md_path: Path,
                        moxfield_path: Path,
                        swaps: List[Dict[str, Any]],
                        reason: str) -> bool:
    """
    Atomically updates:
      1. Main markdown card explanations & category counts
      2. Plain Text Copy/Paste section with strict GFM 2-space line breaks
      3. moxfield_import.txt with raw text
      4. Appends to ## Deck Changelog
    """
    if not md_path or not md_path.exists():
        print(f"Error: Markdown deck file not found at {md_path}", file=sys.stderr)
        return False
    if not moxfield_path or not moxfield_path.exists():
        print(f"Error: moxfield_import.txt not found at {moxfield_path}", file=sys.stderr)
        return False

    md_content = md_path.read_text(encoding="utf-8")
    mox_content = moxfield_path.read_text(encoding="utf-8")

    # 1. Update Moxfield import text
    for s in swaps:
        out_name = s["out"]["name"]
        in_name = s["in"]["name"]

        # Replace 1 OutName with 1 InName in moxfield_import.txt
        pattern = rf'^\s*1\s+{re.escape(out_name)}\s*$'
        new_line = f"1 {in_name}"
        mox_content, count = re.subn(pattern, new_line, mox_content, flags=re.MULTILINE)
        if count == 0:
            # Try case-insensitive fallback
            pattern_ci = rf'^\s*1\s+{re.escape(out_name)}\s*$'
            mox_content, count = re.subn(pattern_ci, new_line, mox_content, flags=re.MULTILINE | re.IGNORECASE)

    # 2. Update Markdown Deck File
    # (a) Card Explanations section
    for s in swaps:
        out_name = s["out"]["name"]
        in_name = s["in"]["name"]
        in_cost = s["in"]["mana_cost"]
        in_uri = s["in"]["scryfall_uri"]
        in_role = s.get("rationale") or f"Replaced {out_name} for improved deck synergy."

        # Search for markdown bullet item matching out_name
        bullet_pattern = rf'^\s*\*\s+\*\*\[?{re.escape(out_name)}(?:\]\([^)]+\))?(?:\s*\([^)]+\))?\s*:\*\*.*$'
        cost_tag = f" ({in_cost})" if in_cost else ""
        replacement_bullet = f"*   **[{in_name}]({in_uri}){cost_tag}:** {in_role}"

        md_content, b_count = re.subn(bullet_pattern, replacement_bullet, md_content, flags=re.MULTILINE)
        if b_count == 0:
            # Fallback for plain bold without link
            bullet_pattern_plain = rf'^\s*\*\s+\*\*{re.escape(out_name)}\*\*.*$'
            md_content, b_count = re.subn(bullet_pattern_plain, replacement_bullet, md_content, flags=re.MULTILINE)

    # (b) Plain Text Copy/Paste section in markdown
    # Each line MUST have two spaces at the end
    plain_text_match = re.search(r'(## [^\n]*Plain Text Copy/Paste[^\n]*\n)(.*?)(\n##|\Z)', md_content, re.DOTALL)
    if plain_text_match:
        pt_header = plain_text_match.group(1)
        pt_body = plain_text_match.group(2)
        pt_trailing = plain_text_match.group(3)

        for s in swaps:
            out_name = s["out"]["name"]
            in_name = s["in"]["name"]
            # Look for 1 OutName  (with optional trailing spaces)
            pt_pat = rf'^(1\s+{re.escape(out_name)})\s*$'
            pt_body = re.sub(pt_pat, rf'1 {in_name}  ', pt_body, flags=re.MULTILINE)

        # Ensure all card lines have 2 trailing spaces
        reformatted_lines = []
        for line in pt_body.splitlines():
            line_str = line.rstrip()
            if line_str and not line_str.startswith("#") and not line_str.startswith("["):
                reformatted_lines.append(line_str + "  ")
            else:
                reformatted_lines.append(line_str)
        updated_pt_body = "\n".join(reformatted_lines)
        md_content = md_content[:plain_text_match.start(2)] + updated_pt_body + md_content[plain_text_match.end(2):]

    # (c) Append to Changelog
    today = time.strftime("%Y-%m-%d")
    in_names_str = ", ".join([s["in"]["name"] for s in swaps])
    out_names_str = ", ".join([s["out"]["name"] for s in swaps])
    changelog_entry = (
        f"- **[{today}]:** {reason}\n"
        f"    - **In:** {in_names_str}\n"
        f"    - **Out:** {out_names_str}\n"
        f"    - **Reason:** {reason}\n"
    )

    changelog_header_match = re.search(r'(## [^\n]*Deck Changelog[^\n]*\n)', md_content)
    if changelog_header_match:
        pos = changelog_header_match.end(1)
        md_content = md_content[:pos] + changelog_entry + md_content[pos:]

    # Write files back atomically
    moxfield_path.write_text(mox_content, encoding="utf-8")
    md_path.write_text(md_content, encoding="utf-8")

    print(f"[apply] Successfully executed Triple Update!")
    print(f"        Updated markdown: {md_path}")
    print(f"        Updated Moxfield: {moxfield_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="MTG Visual Swap Matrix & Mechanics Pre-Check Utility")
    parser.add_argument("deck_path", help="Path to moxfield_import.txt or markdown deck file")
    parser.add_argument("--in", dest="in_cards", nargs="+", required=True, help="Cards to add (supports 'Name: Role')")
    parser.add_argument("--out", dest="out_cards", nargs="+", required=True, help="Cards to cut")
    parser.add_argument("--reason", default="Optimization and deck refinement", help="Summary rationale for swaps")
    parser.add_argument("--bracket", type=int, choices=[1, 2, 3, 4, 5], default=None, help="Commander Bracket (1-5)")
    parser.add_argument("--html", nargs="?", const="__AUTO__", default="__AUTO__", help="Path for HTML visual report")
    parser.add_argument("--apply", action="store_true", help="Atomically apply Triple-Update changes to files")

    args = parser.parse_args()

    moxfield_path, md_path, deck_dir = find_deck_files(args.deck_path)
    if not moxfield_path and not md_path:
        print(f"Error: Could not locate deck files for '{args.deck_path}'", file=sys.stderr)
        sys.exit(1)

    bracket = args.bracket or detect_deck_bracket(md_path)
    commander_name, deck_card_names = parse_moxfield_list(moxfield_path)

    commander_data = get_card_info(commander_name) if commander_name else None

    # Clean and parse IN / OUT inputs
    parsed_in = [clean_card_name(c) for c in args.in_cards]
    parsed_out = [clean_card_name(c) for c in args.out_cards]

    if len(parsed_in) != len(parsed_out):
        print(f"[warning] Count mismatch: {len(parsed_in)} cards IN vs {len(parsed_out)} cards OUT.")

    # Fetch data for all cards
    in_data = [get_card_info(name) for name, cat, role in parsed_in]
    out_data = [get_card_info(name) for name, cat, role in parsed_out]

    # Map swaps
    swaps = []
    for i in range(max(len(in_data), len(out_data))):
        in_c = in_data[i] if i < len(in_data) else get_card_info("Unknown")
        out_c = out_data[i] if i < len(out_data) else get_card_info("Unknown")
        rationale = parsed_in[i][2] if i < len(parsed_in) and parsed_in[i][2] else args.reason
        swaps.append({
            "in": in_c,
            "out": out_c,
            "rationale": rationale
        })

    # Pre-swap deck data
    pre_deck_data = [get_card_info(name) for name in deck_card_names]

    # Post-swap deck list simulation
    post_deck_names = list(deck_card_names)
    for s in swaps:
        out_name = s["out"]["name"]
        in_name = s["in"]["name"]
        # Remove first occurrence of out_name
        found = False
        for idx, name in enumerate(post_deck_names):
            if name.lower() == out_name.lower():
                post_deck_names.pop(idx)
                found = True
                break
        if not found and out_name != "Unknown":
            print(f"[warning] Card to remove '{out_name}' was not found in current deck list.")
        if in_name != "Unknown":
            post_deck_names.append(in_name)

    post_deck_data = [get_card_info(name) for name in post_deck_names]

    # Compute metrics
    pre_metrics = calculate_metrics(pre_deck_data)
    post_metrics = calculate_metrics(post_deck_data)

    # Audit rules
    rules_notes = audit_rules(pre_deck_data, in_data, commander_data, bracket)

    # Print CLI Markdown Output
    deck_name = deck_dir.name
    print(f"\n### 🔄 Proposed Swap Matrix: {deck_name} ({len(swaps)} Cards)\n")
    print(f"| # | Out (Cut) | CMC | Type | In (Add) | CMC | Type | Role & Rationale |")
    print(f"|---|---|---|---|---|---|---|---|")
    for idx, s in enumerate(swaps, start=1):
        o = s["out"]
        i = s["in"]
        print(f"| {idx} | [{o['name']}]({o['scryfall_uri']}) | {o['cmc']} | {o['type_line'].split('—')[0].strip()} | [{i['name']}]({i['scryfall_uri']}) | {i['cmc']} | {i['type_line'].split('—')[0].strip()} | {s['rationale']} |")

    cmc_diff = post_metrics["avg_cmc"] - pre_metrics["avg_cmc"]
    sign = "+" if cmc_diff > 0 else ""
    gc_cnt = len(post_metrics["game_changers"])

    print(f"\n#### 📊 Delta Dashboard")
    print(f"* **Avg CMC:** {pre_metrics['avg_cmc']:.2f} ➔ {post_metrics['avg_cmc']:.2f} ({sign}{cmc_diff:.2f})")
    print(f"* **Curve Shift:** 0-1: {pre_metrics['curve']['0-1']}➔{post_metrics['curve']['0-1']} | 2: {pre_metrics['curve']['2']}➔{post_metrics['curve']['2']} | 3: {pre_metrics['curve']['3']}➔{post_metrics['curve']['3']} | 4: {pre_metrics['curve']['4']}➔{post_metrics['curve']['4']} | 5: {pre_metrics['curve']['5']}➔{post_metrics['curve']['5']} | 6+: {pre_metrics['curve']['6+']}➔{post_metrics['curve']['6+']}")
    print(f"* **Type Balance:** Creatures: {pre_metrics['types']['Creature']}➔{post_metrics['types']['Creature']} | Artifacts: {pre_metrics['types']['Artifact']}➔{post_metrics['types']['Artifact']} | Lands: {post_metrics['types']['Land']}")
    print(f"* **Game Changers:** {gc_cnt} / 3 ({', '.join(post_metrics['game_changers']) or 'None'}) — {'Bracket 3 Compliant' if gc_cnt <= 3 else 'EXCEEDS BRACKET 3 LIMIT'}")
    price_diff = post_metrics["total_price"] - pre_metrics["total_price"]
    psign = "+" if price_diff > 0 else ""
    print(f"* **Est. Value Impact:** {psign}${price_diff:.2f} (${pre_metrics['total_price']:.2f} ➔ ${post_metrics['total_price']:.2f})")

    if rules_notes:
        print(f"\n#### 🛡️ Rules & Synergy Watchdog")
        for r in rules_notes:
            print(f"* **[{r['severity']}] {r['card']}:** {r['message']}")
    else:
        print(f"\n#### 🛡️ Rules & Synergy Watchdog: All Clear (No mechanics traps detected)")

    # HTML Report Generation
    if args.html:
        if args.html == "__AUTO__":
            html_path = deck_dir / "swap_matrix.html"
        else:
            html_path = Path(args.html)
        generate_html_matrix(html_path, deck_name, commander_name or "Commander", bracket,
                             swaps, pre_metrics, post_metrics, rules_notes, args.reason)

    # Atomic Apply
    if args.apply:
        has_critical = any(r["severity"] == "CRITICAL" for r in rules_notes)
        if has_critical:
            print("\n[apply] BLOCKED: Cannot apply swaps due to CRITICAL rule violations (e.g. Color Identity).", file=sys.stderr)
            sys.exit(1)
        apply_triple_update(md_path, moxfield_path, swaps, args.reason)


if __name__ == "__main__":
    main()
