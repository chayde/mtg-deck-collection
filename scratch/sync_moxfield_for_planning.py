import os
import re
from pathlib import Path
from find_main_decks import get_main_deck_file

planning = Path("commander_decks/Planning")

for d in sorted(planning.iterdir()):
    if not d.is_dir():
        continue
    mox = d / "moxfield_import.txt"
    if mox.exists():
        continue
    
    f = get_main_deck_file(d)
    if not f or not f.exists():
        print(f"Skipping {d.name}: No main markdown file")
        continue
        
    content = f.read_text(encoding="utf-8", errors="ignore")
    # Search for Plain Text section
    m = re.search(r"## Plain Text[^\n]*\n(```[^\n]*\n)?(.*?)(\n```|$)", content, re.DOTALL)
    if not m:
        m = re.search(r"Plain Text Copy/Paste[^\n]*\n(```[^\n]*\n)?(.*?)(\n```|$)", content, re.DOTALL)
        
    if m:
        raw_text = m.group(2).strip()
        lines = [l.strip() for l in raw_text.splitlines() if l.strip() and not l.startswith("//") and not l.startswith("#")]
        if len(lines) >= 50:
            mox.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"[EXTRACTED] {d.name:<25} -> {mox.name} ({len(lines)} cards)")
        else:
            print(f"[TOO FEW] {d.name:<25} -> Only {len(lines)} lines found")
    else:
        print(f"[NO SECTION] {d.name:<25} -> Plain text section not found")
