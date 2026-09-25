import re
from pathlib import Path
from find_main_decks import get_main_deck_file

planning = Path("commander_decks/Planning")
for d in sorted(planning.iterdir()):
    if not d.is_dir():
        continue
    f = get_main_deck_file(d)
    if not f or not f.exists():
        continue
    content = f.read_text(encoding="utf-8", errors="ignore")
    m_brk = re.search(r"\*\*Bracket:\*\*\s*([^\n\r]+)", content)
    m_cmd = re.search(r"## Commander Strategy\s*\n\*\*([^\*\n]+)\*\*", content)
    if not m_cmd:
        m_cmd = re.search(r"## (?:1\. )?The Commander\s*\n\*\s*\*\*([^\*\n]+)\*\*", content)
    print(f"{d.name:<28} | File: {f.name:<32} | Cmd: {m_cmd.group(1) if m_cmd else 'N/A':<24} | {m_brk.group(0) if m_brk else 'No Bracket line'}")
