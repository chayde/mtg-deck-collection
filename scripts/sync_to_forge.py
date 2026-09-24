#!/usr/bin/env python3
"""
scripts/sync_to_forge.py — MTG Forge Deck Synchronizer

Synchronizes Commander decks from this repository directly into MTG Forge's
local deck library (%APPDATA%\\Forge\\decks\\commander\\ on Windows).

Eliminates manual imports by serializing decks directly into Forge's native .dck format:
  [metadata]
  Name=<DeckName>
  [Main]
  1 <Card>
  ...
  [Commander]
  1 <Commander>

Usage:
  # Sync a single deck
  python scripts/sync_to_forge.py "commander_decks/Owned/TheHive"

  # Sync all decks in repository
  python scripts/sync_to_forge.py --all

  # Dry-run preview
  python scripts/sync_to_forge.py "commander_decks/Owned/TheHive" --dry-run
"""

import os
import sys
import re
import argparse
import zipfile
import unicodedata
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Set

# Ensure UTF-8 output on Windows consoles
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

# Known mapping between repository folder names and existing Forge .dck deck names
KNOWN_FORGE_ALIASES: Dict[str, str] = {
    "UrDragonKibler": "UrDragon",
    "KarametraAngels": "Karametra",
    "TheHive": "TheHive",
    "SauronGrixis": "Sauron",
    "EtaliConqueror": "Etali",
    "HenzieBlitz": "Henzie",
    "MerenGolgari": "MerenReanimator",
    "RoccoStreetChef": "Rocco",
    "AtraxaPraetorsVoice": "Atraxa SuperFriends",
    "CaesarLegionsEmperor": "Caesar Legion's Emperor",
    "FelotharSteadfast": "FelotharTheSteadfast",
    "GrolnokFrogs": "GrolnakFrogs",
    "MahadiEmporium": "Mahadi",
    "NekusarMindrazer": "Nekusar",
    "RamsesAssassinLord": "Ramses-Assassins",
    "SvellaIceShaper": "Svella",
    "TheNecrobloom": "The Necrobloom",
    "UltronArtificialMalevolence": "Ultron",
    "ZangiefJundAttritron": "Zangief",
    "YidrisChaos": "YidrisCascade",
    "EdgarMarkov": "Vampires",
    "IncredibleHulk": "Gamma Smash",
    "CaptainAmerica": "Captain America",
    "QuantumQuandrix": "Quantum Quandrix",
    "ChainerDementiaMaster": "Chainer",
    "EmperorPalamecia": "Emperor Palamecia",
    "GreenGoblin": "Green Goblin",
    "SyggRiverCutthroat": "Sygg",
    "UlalekFusedAtrocity": "Ulalek",
    "RafiqBant": "Rafiq",
    "KrenkoMobBoss": "Krenko",
    "GisaTheHellraiser": "Gisa The Hellraiser",
    "KrenkoBracket3": "Krenko Bracket 3",
}


def get_default_forge_commander_dir() -> Optional[Path]:
    """
    Locates the Forge commander decks directory.
    Checks environment variable, Windows APPDATA, and typical user paths.
    """
    env_dir = os.environ.get("FORGE_COMMANDER_DECKS")
    if env_dir:
        p = Path(env_dir)
        if p.exists() or p.parent.exists():
            return p

    # Windows AppData
    appdata = os.environ.get("APPDATA")
    if appdata:
        p = Path(appdata) / "Forge" / "decks" / "commander"
        if p.exists() or (Path(appdata) / "Forge").exists():
            return p

    # User Home fallback
    home = Path.home()
    user_forge = home / "AppData" / "Roaming" / "Forge" / "decks" / "commander"
    if user_forge.exists():
        return user_forge

    # Linux / macOS fallback
    dot_forge = home / ".forge" / "decks" / "commander"
    if dot_forge.exists():
        return dot_forge

    # Program directory fallback
    prog_forge = Path("C:/forge-mtg/res/decks/commander")
    if prog_forge.exists():
        return prog_forge

    return None


def resolve_deck_files(target: Path) -> Tuple[Optional[Path], Optional[Path], Path]:
    """
    Given a target path (directory, .md file, or moxfield_import.txt),
    returns (moxfield_path, md_path, deck_dir).
    """
    if target.is_file():
        deck_dir = target.parent
        if target.name == "moxfield_import.txt":
            moxfield_path = target
            md_files = [f for f in deck_dir.glob("*.md") if f.name not in {"order_tracking.md", "GOLDFISH_LOG.md"}]
            md_path = md_files[0] if md_files else None
            return moxfield_path, md_path, deck_dir
        else:
            md_path = target
            moxfield_path = deck_dir / "moxfield_import.txt"
            return moxfield_path if moxfield_path.exists() else None, md_path, deck_dir
    elif target.is_dir():
        deck_dir = target
        moxfield_path = deck_dir / "moxfield_import.txt"
        md_files = [f for f in deck_dir.glob("*.md") if f.name not in {"order_tracking.md", "GOLDFISH_LOG.md"}]
        md_path = md_files[0] if md_files else None
        return moxfield_path if moxfield_path.exists() else None, md_path, deck_dir
    else:
        return None, None, target


_FORGE_CARD_CACHE: Optional[Tuple[Set[str], Dict[str, str]]] = None


def strip_accents(s: str) -> str:
    """Removes diacritics/accents from a string (e.g. 'Andúril' -> 'Anduril')."""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def find_forge_cardsfolder_zip() -> Optional[Path]:
    """
    Locates Forge's cardsfolder.zip containing official card definitions.
    """
    env_forge = os.environ.get("FORGE_INSTALL_DIR") or os.environ.get("FORGE_DIR")
    if env_forge:
        p = Path(env_forge) / "res" / "cardsfolder" / "cardsfolder.zip"
        if p.exists():
            return p

    candidates = [
        Path("C:/forge-mtg/res/cardsfolder/cardsfolder.zip"),
        Path("C:/forge/res/cardsfolder/cardsfolder.zip"),
        Path.home() / "forge-mtg" / "res" / "cardsfolder" / "cardsfolder.zip",
        Path.home() / "forge" / "res" / "cardsfolder" / "cardsfolder.zip",
        Path.home() / "AppData" / "Local" / "Forge" / "res" / "cardsfolder" / "cardsfolder.zip",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def get_forge_card_db() -> Tuple[Set[str], Dict[str, str]]:
    """
    Loads all valid card names from Forge's cardsfolder.zip into memory.
    Returns:
      (exact_names_set, lookup_dict) where lookup_dict maps lowercased and
      accent-stripped names to Forge's primary face name.
    """
    global _FORGE_CARD_CACHE
    if _FORGE_CARD_CACHE is not None:
        return _FORGE_CARD_CACHE

    exact_names: Set[str] = set()
    lookup: Dict[str, str] = {}

    zip_path = find_forge_cardsfolder_zip()
    if zip_path and zip_path.exists():
        try:
            with zipfile.ZipFile(zip_path) as z:
                for fname in z.namelist():
                    if fname.endswith('.txt'):
                        try:
                            content = z.read(fname).decode('utf-8', errors='ignore')
                            lines = content.splitlines()
                            primary_name = None
                            for line in lines:
                                if line.startswith('Name:'):
                                    name = line[5:].strip()
                                    if primary_name is None:
                                        primary_name = name
                                    exact_names.add(name)
                                    lookup[name.lower()] = primary_name
                                    lookup[strip_accents(name.lower())] = primary_name
                        except Exception:
                            pass
        except Exception:
            pass

    _FORGE_CARD_CACHE = (exact_names, lookup)
    return _FORGE_CARD_CACHE


def sanitize_card_for_forge(
    raw_card_line: str,
    lookup: Optional[Dict[str, str]] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Sanitizes a raw card line (e.g. '1 Norman Osborn / Green Goblin *CMDR*') into
    a Forge-compatible card line (e.g. '1 Norman Osborn').
    Returns (formatted_card_line, warning_message).
    Returns (None, None) if the card should be skipped (e.g. tokens, emblems).
    """
    cleaned_line = re.sub(r'\s*\*[A-Za-z0-9_-]+\*', '', raw_card_line).strip()
    m = re.match(r'^(\d+\s+)?(.*)$', cleaned_line)
    if not m:
        return None, None

    qty = m.group(1) or "1 "
    card_name = m.group(2).strip()
    if not card_name:
        return None, None

    # Filter out tokens, emblems, and auxiliary objects not in the 99/Commander
    lower = card_name.lower()
    if 'token' in lower or 'emblem' in lower or lower == 'the ring tempts you':
        return None, None

    # Preserve edition / collector number suffix if present (e.g. "Card|SET|[123]")
    if '|' in card_name:
        parts = card_name.split('|', 1)
        base_name = parts[0].strip()
        edition_suffix = "|" + parts[1]
    else:
        base_name = card_name
        edition_suffix = ""

    warning: Optional[str] = None
    target_name = base_name

    if lookup:
        base_lower = base_name.lower()
        base_unaccented = strip_accents(base_lower)

        if base_lower in lookup:
            target_name = lookup[base_lower]
        elif base_unaccented in lookup:
            target_name = lookup[base_unaccented]
        elif '/' in base_name:
            # Multi-faced cards (DFCs, MDFCs, split cards, adventures)
            # In Forge, these cards are indexed strictly by their primary front face
            front_face = re.split(r'\s+[/]+\s+', base_name)[0].strip()
            front_lower = front_face.lower()
            front_unaccented = strip_accents(front_lower)
            if front_lower in lookup:
                target_name = lookup[front_lower]
            elif front_unaccented in lookup:
                target_name = lookup[front_unaccented]
            else:
                target_name = front_face
                warning = f"Card '{base_name}' front-face '{front_face}' not found in Forge database."
        else:
            warning = f"Card '{base_name}' not found in Forge database."
    else:
        # Fallback if Forge cardsfolder is unavailable: split on ' / ' or ' // '
        if '/' in base_name:
            target_name = re.split(r'\s+[/]+\s+', base_name)[0].strip()

    return f"{qty.strip()} {target_name}{edition_suffix}", warning


def parse_deck_list(
    moxfield_path: Optional[Path],
    md_path: Optional[Path],
    lookup: Optional[Dict[str, str]] = None
) -> Tuple[List[str], List[str], List[str]]:
    """
    Extracts commander list and mainboard list, sanitizing cards for Forge.
    Returns: (commanders, mainboard, warnings)
    """
    commanders: List[str] = []
    mainboard: List[str] = []
    warnings: List[str] = []

    if moxfield_path and moxfield_path.exists():
        content = moxfield_path.read_text(encoding="utf-8")
        current_section = "main"

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            header_key = re.sub(r'[^a-z0-9]', '', line.lower())
            if header_key in {"commander", "commanders"}:
                current_section = "commander"
                continue
            elif header_key in {"deck", "main", "maindeck", "mainboard"}:
                current_section = "main"
                continue
            elif header_key in {"sideboard", "maybeboard"}:
                current_section = "sideboard"
                continue

            # Check for *CMDR* tag on card line
            is_cmdr_line = "*cmdr*" in line.lower()
            formatted, warn = sanitize_card_for_forge(line, lookup=lookup)
            if warn:
                warnings.append(warn)
            if not formatted:
                continue

            if current_section == "commander" or is_cmdr_line:
                commanders.append(formatted)
            elif current_section == "main":
                mainboard.append(formatted)

        if commanders or mainboard:
            return commanders, mainboard, warnings

    # Fallback to Markdown Plain Text Copy/Paste section
    if md_path and md_path.exists():
        content = md_path.read_text(encoding="utf-8")
        pt_match = re.search(r'(?:##\s+.*?Plain Text Copy/Paste.*?)(.*?)(?:\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if pt_match:
            pt_text = pt_match.group(1)
            for line in pt_text.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("```"):
                    continue
                formatted, warn = sanitize_card_for_forge(line, lookup=lookup)
                if warn:
                    warnings.append(warn)
                if not formatted:
                    continue
                mainboard.append(formatted)

        # Try to identify commander from markdown header or frontmatter
        cmdr_match = re.search(r'#\s+([^—\n]+?)(?:\s+—|\n)', content)
        if cmdr_match:
            raw_cmdr_name = cmdr_match.group(1).strip()
            formatted_cmdr, warn = sanitize_card_for_forge(f"1 {raw_cmdr_name}", lookup=lookup)
            if warn:
                warnings.append(warn)
            clean_cmdr = formatted_cmdr or f"1 {raw_cmdr_name}"
            # If commander was put in mainboard, move it to commanders
            cmdr_base = re.sub(r'^\d+\s+', '', clean_cmdr).lower()
            for idx, c in enumerate(mainboard):
                if cmdr_base in c.lower():
                    commanders.append(mainboard.pop(idx))
                    break
            if not commanders:
                commanders.append(clean_cmdr)

    return commanders, mainboard, warnings


def determine_forge_deck_name(deck_dir: Path, forge_dir: Path) -> str:
    """
    Determines the Forge deck name and filename.
    1. Checks KNOWN_FORGE_ALIASES.
    2. Checks if an existing .dck file in forge_dir matches folder name prefix.
    3. Falls back to folder name.
    """
    folder_name = deck_dir.name

    # 1. Alias map
    if folder_name in KNOWN_FORGE_ALIASES:
        return KNOWN_FORGE_ALIASES[folder_name]

    # 2. Match existing file in Forge directory
    if forge_dir and forge_dir.exists():
        existing_files = list(forge_dir.glob("*.dck"))
        # Exact stem match
        for f in existing_files:
            if f.stem.lower() == folder_name.lower():
                return f.stem
        # Prefix match (e.g. "Karametra" matches "KarametraAngels")
        for f in existing_files:
            if f.stem.lower() in folder_name.lower() or folder_name.lower() in f.stem.lower():
                return f.stem

    # 3. Fallback
    return folder_name


def serialize_forge_dck(deck_name: str, commanders: List[str], mainboard: List[str]) -> str:
    """
    Formats the deck into Forge's native .dck INI structure.
    Forge native format places [Main] first, then [Commander] at the bottom.
    """
    lines: List[str] = []
    lines.append("[metadata]")
    lines.append(f"Name={deck_name}")

    lines.append("[Main]")
    for c in mainboard:
        lines.append(c)

    if commanders:
        lines.append("[Commander]")
        for c in commanders:
            lines.append(c)

    return "\n".join(lines) + "\n"


def sync_deck_to_forge(
    deck_path_input: str | Path,
    forge_dir: Optional[Path] = None,
    dry_run: bool = False
) -> Tuple[bool, str]:
    """
    Programmatic entrypoint to sync a single deck to Forge.
    Returns: (success: bool, status_message: str)
    """
    target = Path(deck_path_input).resolve()
    moxfield_path, md_path, deck_dir = resolve_deck_files(target)

    if not moxfield_path and not md_path:
        return False, f"Could not find deck files at '{deck_path_input}'."

    target_forge_dir = forge_dir or get_default_forge_commander_dir()
    if not target_forge_dir:
        return False, "Could not determine MTG Forge commander directory (%APPDATA%\\Forge\\decks\\commander\\)."

    _, lookup = get_forge_card_db()
    commanders, mainboard, warnings = parse_deck_list(moxfield_path, md_path, lookup=lookup)
    if not commanders and not mainboard:
        return False, f"No cards could be parsed from deck at '{deck_dir}'."

    deck_name = determine_forge_deck_name(deck_dir, target_forge_dir)
    dck_content = serialize_forge_dck(deck_name, commanders, mainboard)
    out_file = target_forge_dir / f"{deck_name}.dck"

    total_cards = len(commanders) + sum(int(re.match(r'^(\d+)', c).group(1)) if re.match(r'^(\d+)', c) else 1 for c in mainboard)

    warn_str = f" (Warnings: {'; '.join(warnings)})" if warnings else ""

    if dry_run:
        msg = (
            f"[dry-run] Would write {out_file}\n"
            f"          Deck Name: '{deck_name}'\n"
            f"          Commanders: {len(commanders)} | Mainboard: {len(mainboard)} | Total Cards: {total_cards}{warn_str}"
        )
        return True, msg

    try:
        target_forge_dir.mkdir(parents=True, exist_ok=True)
        out_file.write_text(dck_content, encoding="utf-8")
        msg = f"Synced '{deck_name}' ({total_cards} cards) ➔ {out_file}{warn_str}"
        return True, msg
    except Exception as e:
        return False, f"Failed to write Forge deck file '{out_file}': {e}"


def find_all_commander_decks(repo_root: Path) -> List[Path]:
    """
    Finds all valid Commander deck directories in commander_decks/.
    """
    base_dir = repo_root / "commander_decks"
    decks = []
    if not base_dir.exists():
        return decks

    for p in base_dir.rglob("moxfield_import.txt"):
        deck_dir = p.parent
        # Skip archive or helper folders if any
        if "archive" in deck_dir.parts:
            continue
        decks.append(deck_dir)

    return sorted(decks, key=lambda d: d.name)


def main():
    parser = argparse.ArgumentParser(description="Synchronize Commander decks to MTG Forge")
    parser.add_argument("deck_path", nargs="?", default=None, help="Path to deck folder, markdown file, or moxfield_import.txt")
    parser.add_argument("--all", action="store_true", help="Sync all Commander decks in commander_decks/")
    parser.add_argument("--forge-dir", type=str, default=None, help="Custom Forge commander decks directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview output without writing files")

    args = parser.parse_args()

    forge_dir = Path(args.forge_dir) if args.forge_dir else get_default_forge_commander_dir()
    if not forge_dir:
        print("Error: Could not locate Forge commander deck directory.", file=sys.stderr)
        print("Ensure Forge is installed or specify --forge-dir '<path>'", file=sys.stderr)
        sys.exit(1)

    print(f"[Forge] Target Directory: {forge_dir}\n")

    if args.all:
        decks = find_all_commander_decks(REPO_ROOT)
        if not decks:
            print("No decks found in commander_decks/", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(decks)} Commander decks to sync:")
        success_count = 0
        for d in decks:
            success, msg = sync_deck_to_forge(d, forge_dir=forge_dir, dry_run=args.dry_run)
            prefix = "OK" if success else "FAIL"
            print(f"  [{prefix}] {msg}")
            if success:
                success_count += 1

        print(f"\n[Forge] Sync Complete: {success_count}/{len(decks)} decks synced successfully.")
    else:
        if not args.deck_path:
            print("Error: Specify a deck path or use --all to sync all decks.", file=sys.stderr)
            parser.print_help()
            sys.exit(1)

        success, msg = sync_deck_to_forge(args.deck_path, forge_dir=forge_dir, dry_run=args.dry_run)
        if success:
            print(f"[OK] {msg}")
        else:
            print(f"[ERROR] {msg}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
