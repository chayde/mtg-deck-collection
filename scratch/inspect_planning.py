import os
import re
from pathlib import Path
from find_main_decks import get_main_deck_file

planning = Path("commander_decks/Planning")
for d in sorted(planning.iterdir()):
    if not d.is_dir():
        continue
    f = get_main_deck_file(d)
    mox = d / "moxfield_import.txt"
    has_mox = mox.exists()
    card_count = 0
    if has_mox:
        lines = [l.strip() for l in mox.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip() and not l.startswith("//") and not l.startswith("#") and l not in ("COMMANDER:", "DECK:")]
        card_count = len(lines)
    
    # Check if main md has plain text section
    has_plain_text = False
    if f and f.exists():
        content = f.read_text(encoding="utf-8", errors="ignore")
        if "## Plain Text" in content or "Plain Text Copy/Paste" in content:
            has_plain_text = True
            
    print(f"{d.name:<28} | File: {f.name if f else 'None':<32} | Mox: {has_mox} ({card_count}) | PlainText: {has_plain_text}")
