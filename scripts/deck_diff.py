#!/usr/bin/env python3
"""
deck_diff.py — MTG Deck Cross-Referencing & Acquisition Tracking Utility

This script compares a target deck list against one or more sources (an existing deck,
a precon list, and/or collection.csv) to determine:
  1. Which cards are already owned / in-hand.
  2. Which cards are missing and need to be acquired.
  3. Formats the results for terminal display or generates a complete order_tracking.md checklist.

Usage:
  python3 scripts/deck_diff.py <target_deck> [--source <source_deck>] [--collection [collection.csv]] [--output-tracking <path>]

Examples:
  # Compare target deck against a precon:
  python3 scripts/deck_diff.py "commander_decks/Planning/UlalekFusedAtrocity/moxfield_import.txt" \
      --source "commander_decks/Owned/PreCons/UlalekFusedAtrocity/Ulalek_Fused_Atrocity.txt"

  # Compare target deck against physical collection database:
  python3 scripts/deck_diff.py "commander_decks/Planning/UlalekFusedAtrocity/moxfield_import.txt" \
      --collection collection.csv

  # Compare target deck against both a precon and collection.csv, and update order_tracking.md:
  python3 scripts/deck_diff.py "commander_decks/Planning/UlalekFusedAtrocity/moxfield_import.txt" \
      --source "commander_decks/Owned/PreCons/UlalekFusedAtrocity/Ulalek_Fused_Atrocity.txt" \
      --collection \
      --output-tracking "commander_decks/Planning/UlalekFusedAtrocity/order_tracking.md"
"""

import argparse
import csv
import json
import os
import re
import sys

BASIC_LANDS = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes"}

def load_card_cache():
    """Attempts to load Scryfall cache from local disk for card type categorization."""
    cache_paths = [
        os.path.join("cache", "scryfall_cards.json"),
        os.path.join("scripts", ".card_cache.json")
    ]
    cache = {}
    for p in cache_paths:
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        # Handle either raw card object or wrapped in {"data": ...}
                        if isinstance(v, dict):
                            card_data = v.get("data", v)
                            cache[k.lower()] = card_data
            except Exception:
                pass
    return cache

def extract_card_name(line):
    """
    Cleans and extracts a canonical MTG card name from various formats:
      - '1x Sol Ring (cmm) 305'
      - '1 Sol Ring'
      - '* **Sol Ring:** Ramp piece'
      - 'Sol Ring'
    """
    line = line.strip()
    if not line:
        return None
    if line.startswith("//") or line.startswith("#") or line in [
        "Commander", "Artifact", "Creature", "Enchantment", "Instant", "Sorcery",
        "Planeswalker", "Land", "COMMANDER:", "DECK:", "SIDEBOARD:", "MAIN DECK:",
        "MAIN DECK", "Main Deck:", "Main Deck", "Commander:"
    ]:
        return None

    # Handle markdown bold list format: * **Card Name:** Description
    m_md = re.match(r"^\*?\s*\*\*([^:\*]+)\*\*", line)
    if m_md:
        return m_md.group(1).strip()

    # Handle count prefix + optional set code: '1x Card Name (set) 123' or '1 Card Name'
    m_count = re.match(r"^\d+x?\s+(.+?)(?:\s+\([a-zA-Z0-9_-]+\)\s+\S+)?$", line)
    if m_count:
        name = m_count.group(1).strip()
        # strip trailing set codes like '(m3c) 4' if matched inside
        name = re.sub(r"\s+\([a-zA-Z0-9_-]+\)\s+\S+$", "", name).strip()
        return name

    # Strip any trailing (set) 123
    cleaned = re.sub(r"\s+\([a-zA-Z0-9_-]+\)\s+\S+$", "", line).strip()
    return cleaned if cleaned else None

def parse_deck_file(file_path):
    """Parses a text or markdown deck file and returns a list of card names."""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    cards = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        in_plain_text = False
        lines = f.readlines()

        # If it's a markdown file with a Plain Text section, prefer that section
        has_plain_text_header = any("Plain Text Copy/Paste" in l or "COMMANDER:" in l for l in lines)
        
        for line in lines:
            line_str = line.strip()
            if has_plain_text_header:
                if "COMMANDER:" in line_str or "Plain Text Copy/Paste" in line_str:
                    in_plain_text = True
                    continue
                if in_plain_text:
                    if line_str.startswith("SIDEBOARD:"):
                        break
                    card = extract_card_name(line)
                    if card:
                        cards.append(card)
            else:
                card = extract_card_name(line)
                if card:
                    cards.append(card)

    return cards

def parse_collection_csv(csv_path="collection.csv"):
    """Parses collection.csv and returns a set of owned card names."""
    if not os.path.exists(csv_path):
        print(f"Warning: Collection file '{csv_path}' not found.", file=sys.stderr)
        return set()

    owned = set()
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Name", "").strip()
            qty = row.get("Quantity", "1").strip()
            try:
                count = int(qty)
            except ValueError:
                count = 1
            if name and count > 0:
                owned.add(name)
    return owned

def categorize_cards(card_names, card_cache):
    """Categorizes cards into broad MTG categories using cache or fallback rules."""
    categories = {
        "Lands": [],
        "Creatures": [],
        "Artifacts & Ramp": [],
        "Spells & Interaction": [],
        "Enchantments & Planeswalkers": [],
        "Other": []
    }

    for name in card_names:
        lower = name.lower()
        cached = card_cache.get(lower) or {}
        type_line = cached.get("type_line", "") or cached.get("type", "")

        if "land" in type_line.lower() or name in BASIC_LANDS:
            categories["Lands"].append(name)
        elif "creature" in type_line.lower():
            categories["Creatures"].append(name)
        elif "artifact" in type_line.lower():
            categories["Artifacts & Ramp"].append(name)
        elif any(t in type_line.lower() for t in ["instant", "sorcery"]):
            categories["Spells & Interaction"].append(name)
        elif any(t in type_line.lower() for t in ["enchantment", "planeswalker"]):
            categories["Enchantments & Planeswalkers"].append(name)
        else:
            # Simple heuristic fallbacks if un-cached
            if any(term in lower for term in ["land", "wastes", "forest", "island", "mountain", "plains", "swamp", "tomb", "cavern", "temple", "reef", "springs"]):
                categories["Lands"].append(name)
            elif any(term in lower for term in ["talisman", "signet", "sol ring", "monolith", "monument", "boots", "greaves"]):
                categories["Artifacts & Ramp"].append(name)
            else:
                categories["Other"].append(name)

    # Sort each category
    for cat in categories:
        categories[cat] = sorted(categories[cat])

    return categories

def format_tracking_markdown(deck_name, owned_cards, missing_cards, card_cache):
    """Generates a complete order_tracking.md formatted string."""
    categorized_missing = categorize_cards(missing_cards, card_cache)
    
    total = len(owned_cards) + len(missing_cards)
    out = [
        f"# Order Tracking: {deck_name}",
        "",
        "## Overview",
        f"*   **Total Deck Size:** {total} Cards",
        f"*   **In-Hand / Owned:** {len(owned_cards)} cards",
        f"*   **Pending Acquisition / Singles to Order:** {len(missing_cards)} cards",
        "",
        "---",
        "",
        f"## 📦 Singles to Acquire / Order List ({len(missing_cards)} Cards)",
        ""
    ]

    for cat_name, items in categorized_missing.items():
        if items:
            out.append(f"### {cat_name} ({len(items)} Cards)")
            for item in items:
                out.append(f"- [ ] {item}")
            out.append("")

    out.append("---")
    out.append("")
    out.append(f"## 🛡️ Inventory In-Hand ({len(owned_cards)} Cards)")
    for item in sorted(owned_cards):
        out.append(f"- [x] {item}")
    out.append("")

    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(
        description="Cross-reference a target deck list against precons, other decks, or collection.csv."
    )
    parser.add_argument("target", help="Path to the target deck file (.txt or .md)")
    parser.add_argument("--source", "-s", action="append", help="Path to one or more source deck/precon files")
    parser.add_argument("--collection", "-c", nargs="?", const="collection.csv", help="Path to collection.csv (default: collection.csv)")
    parser.add_argument("--output-tracking", "-o", help="Path to write or update order_tracking.md")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()

    # 1. Parse target deck
    target_cards = parse_deck_file(args.target)
    if not target_cards:
        print(f"Error: No cards parsed from target deck '{args.target}'", file=sys.stderr)
        sys.exit(1)

    target_set = set(target_cards)
    commander_name = target_cards[0] if target_cards else "Commander Deck"

    # 2. Build owned set from all specified sources
    owned_source_set = set()

    if args.source:
        for src in args.source:
            src_cards = parse_deck_file(src)
            owned_source_set.update(src_cards)

    if args.collection:
        coll_cards = parse_collection_csv(args.collection)
        owned_source_set.update(coll_cards)

    # 3. Compute owned vs missing
    owned_in_target = target_set.intersection(owned_source_set)
    missing_in_target = target_set - owned_source_set

    card_cache = load_card_cache()

    # 4. Handle Output
    if args.json:
        result = {
            "target": args.target,
            "total_cards": len(target_set),
            "owned_count": len(owned_in_target),
            "missing_count": len(missing_in_target),
            "owned": sorted(list(owned_in_target)),
            "missing": sorted(list(missing_in_target))
        }
        print(json.dumps(result, indent=2))
        return

    # Print Terminal Summary
    print("=" * 65)
    print(f"DECK CROSS-REFERENCE AUDIT: {os.path.basename(args.target)}")
    print("=" * 65)
    print(f"  Total Unique Cards:   {len(target_set)}")
    print(f"  In-Hand / Owned:      {len(owned_in_target)} ({len(owned_in_target)/len(target_set)*100:.1f}%)")
    print(f"  Missing / To Order:   {len(missing_in_target)} ({len(missing_in_target)/len(target_set)*100:.1f}%)")
    print("-" * 65)

    if missing_in_target:
        print(f"\n[!] MISSING SINGLES TO ACQUIRE ({len(missing_in_target)}):")
        categorized = categorize_cards(missing_in_target, card_cache)
        for cat, items in categorized.items():
            if items:
                print(f"\n  -- {cat} ({len(items)}) --")
                for c in items:
                    print(f"    - [ ] {c}")
    else:
        print("\n[OK] 100% of cards are in-hand and accounted for!")

    if args.output_tracking:
        deck_title = os.path.basename(os.path.dirname(os.path.abspath(args.output_tracking)))
        if not deck_title or deck_title == "Planning":
            deck_title = os.path.basename(args.target).replace(".txt", "").replace(".md", "")
        md_content = format_tracking_markdown(deck_title, owned_in_target, missing_in_target, card_cache)
        os.makedirs(os.path.dirname(os.path.abspath(args.output_tracking)), exist_ok=True)
        with open(args.output_tracking, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"\n[OK] Updated order tracking file: {args.output_tracking}")

if __name__ == "__main__":
    main()
