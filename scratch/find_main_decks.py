import os
import re
from pathlib import Path

def get_main_deck_file(folder: Path):
    md_files = [f for f in folder.glob("*.md") if f.name not in ("README.md", "order_tracking.md", "GOLDFISH_LOG.md", "dti_audit.md", "OriginalPrompt.md", "price_analysis.md", "optimization_log.md", "deck_analysis.md", "mechanics.md", "sideboard_analysis.md", "GOLDFISH_LOG_OLD.md")]
    if not md_files:
        readme = folder / "README.md"
        if readme.exists():
            content = readme.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"deck_status:\s*main", content, re.IGNORECASE):
                return readme
        return None
    # Look for deck_status: main
    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"deck_status:\s*main", content, re.IGNORECASE):
            return f
    # If no deck_status: main, pick first or match folder name
    for f in md_files:
        if f.stem.lower() in folder.name.lower() or folder.name.lower() in f.stem.lower():
            return f
    return md_files[0]

print("=== OWNED DECKS ===")
owned = Path("commander_decks/Owned")
for d in sorted(owned.iterdir()):
    if not d.is_dir() or d.name == "PreCons":
        continue
    f = get_main_deck_file(d)
    mox = (d / "moxfield_import.txt").exists()
    print(f"{d.name:<22} | Main MD: {f.name if f else 'None':<32} | Moxfield: {mox}")

print("\n=== PLANNING DECKS ===")
planning = Path("commander_decks/Planning")
for d in sorted(planning.iterdir()):
    if not d.is_dir():
        continue
    f = get_main_deck_file(d)
    mox = (d / "moxfield_import.txt").exists()
    print(f"{d.name:<22} | Main MD: {f.name if f else 'None':<32} | Moxfield: {mox}")
