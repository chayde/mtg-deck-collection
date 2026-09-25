import re
from pathlib import Path
from find_main_decks import get_main_deck_file

owned = Path("commander_decks/Owned")
for d in sorted(owned.iterdir()):
    if not d.is_dir() or d.name == "PreCons":
        continue
    f = get_main_deck_file(d)
    content = f.read_text(encoding="utf-8", errors="ignore")
    m_brk = re.search(r"\*\*Bracket:\*\*\s*([^\n\r]+)", content)
    m_cmd = re.search(r"## Commander Strategy\s*\n\*\*([^\*\n]+)\*\*", content)
    mox = d / "moxfield_import.txt"
    lines = [l.strip() for l in mox.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip() and not l.startswith("//")]
    print(f"{d.name:<18} | File: {f.name:<28} | Cmd: {m_cmd.group(1) if m_cmd else 'N/A':<28} | {m_brk.group(0) if m_brk else 'No Bracket line'}")
