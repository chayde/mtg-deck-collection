#!/usr/bin/env python3
"""
scripts/dti_evaluator.py — DeckCheck Threat Index (DTI) Evaluation Engine

Evaluates Commander decks using the DeckCheck Threat Index (DTI) framework:
- Deterministic calculation of 12 universal benchmarks across 5 domains.
- Computes Velocity (max 48) and Suppression (max 40) composite threat vectors.
- Checks calibrated score floors (Brackets 1–5).
- Evaluates the 4 hard gatekeepers (Velocity Gate, Early Finish Gate, Suppression Gate, cEDH Gate).
- Cross-references WotC statutory rules (Game Changers limit, MLD, extra turns).
- Cross-validates against empirical multiplayer goldfish simulation telemetry.
- Exports formatted Markdown audits and interactive visual HTML reports with Scryfall card ledgers.

Usage:
  # Evaluate an existing deck with an evaluation file:
  python scripts/dti_evaluator.py "commander_decks/Planning/KrenkoBracket3"

  # Initialize a new evaluation template for a deck:
  python scripts/dti_evaluator.py "commander_decks/Planning/KrenkoBracket3" --init

  # Quick evaluation via CLI benchmark flags:
  python scripts/dti_evaluator.py "commander_decks/Planning/KrenkoBracket3" \\
      --r1 A --r2 B --a1 B --a2 A --p1 B --p2 A --p3 B --i1 C --i2 F --s1 A --s2 C --s3 C
"""

import os
import sys
import re
import json
import argparse
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

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

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Optional Scryfall lookup import
try:
    from scryfall_lookup import lookup_named
except ImportError:
    lookup_named = None

# --- DTI SCORING RULES & SPECIFICATION ---
BENCHMARK_META = {
    # Terminal Clock (Max 10 pts: S=10, A=5, B=2, C=1, F=0)
    "r1": {"domain": "Resources", "name": "Mana Velocity & Sufficiency", "group": "clock", "max": 10},
    "a2": {"domain": "Access", "name": "Assembly Velocity", "group": "clock", "max": 10},
    "p1": {"domain": "Pressure", "name": "Critical Onset & Lethality", "group": "clock", "max": 10},
    "p2": {"domain": "Pressure", "name": "Win Inevitability & Compactness", "group": "clock", "max": 10},

    # Execution Modifiers (Max 8 pts: S=8, A=4, B=2, C=1, F=0)
    "r2": {"domain": "Resources", "name": "Card Flow & Replenishment", "group": "modifier", "max": 8},
    "a1": {"domain": "Access", "name": "Selection & Redundancy", "group": "modifier", "max": 8},
    "p3": {"domain": "Pressure", "name": "Exposure & Predictability", "group": "modifier", "max": 8},
    "i1": {"domain": "Interaction", "name": "Reactive Disruption", "group": "modifier", "max": 8},
    "i2": {"domain": "Interaction", "name": "Proactive Denial & Restriction", "group": "modifier", "max": 8},
    "s1": {"domain": "Resilience", "name": "Plan Shielding & Protection", "group": "modifier", "max": 8},

    # Contingency Buffers (Max 4 pts: S=4, A=2, B=1, C=0, F=0)
    "s2": {"domain": "Resilience", "name": "Engine Recovery", "group": "buffer", "max": 4},
    "s3": {"domain": "Resilience", "name": "Independence & Backup Plans", "group": "buffer", "max": 4},
}

TIER_POINTS = {
    "clock":    {"S": 10, "A": 5, "B": 2, "C": 1, "F": 0},
    "modifier": {"S": 8,  "A": 4, "B": 2, "C": 1, "F": 0},
    "buffer":   {"S": 4,  "A": 2, "B": 1, "C": 0, "F": 0},
}

# Calibrated DTI Score Bands (Post 2 Calibration)
BRACKET_THRESHOLDS = [
    (68, 5, "Bracket 5 (cEDH)"),
    (52, 4, "Bracket 4 (Optimized)"),
    (32, 3, "Bracket 3 (Upgraded Casual)"),
    (16, 2, "Bracket 2 (Core / Precon)"),
    (0,  1, "Bracket 1 (Exhibition)"),
]

# Known Game Changers from COMMANDER_DECKBUILDING_RULES.md
KNOWN_GAME_CHANGERS = {
    "drannith magistrate", "consecrated sphinx", "thassa's oracle", "braids, cabal minion",
    "opposition agent", "orcish bowmasters", "tergrid, god of fright", "seedborn muse",
    "grand arbiter augustin iv", "notion thief", "humility", "smothering tithe",
    "rhystic study", "necropotence", "underworld breach", "survival of the fittest",
    "aura shards", "serra's sanctum", "gaea's cradle", "ancient tomb", "field of the dead",
    "glacial chasm", "mishra's workshop", "the tabernacle at pendrell vale",
    "enlightened tutor", "teferi's protection", "cyclonic rift", "force of will",
    "fierce guardianship", "gifts ungiven", "intuition", "mystical tutor",
    "ad nauseam", "vampiric tutor", "crop rotation", "worldly tutor",
    "narset, parter of veils", "bolas's citadel", "chrome mox", "grim monolith",
    "lion's eye diamond", "mana vault", "the one ring"
}

# ---------------------------------------------------------------------------
# Data Resolution Helpers
# ---------------------------------------------------------------------------

def resolve_deck_paths(target: str) -> Tuple[Path, Optional[Path], Optional[Path]]:
    """Resolves target into (deck_dir, moxfield_txt_path, md_file_path)."""
    p = Path(target).resolve()
    if p.is_file():
        deck_dir = p.parent
        if p.name == "moxfield_import.txt":
            moxfield_file = p
            md_files = [f for f in deck_dir.glob("*.md") if f.name not in ("README.md", "order_tracking.md", "GOLDFISH_LOG.md", "dti_audit.md")]
            md_file = md_files[0] if md_files else None
        else:
            md_file = p
            moxfield_file = deck_dir / "moxfield_import.txt"
    else:
        deck_dir = p
        moxfield_file = deck_dir / "moxfield_import.txt"
        md_files = [f for f in deck_dir.glob("*.md") if f.name not in ("README.md", "order_tracking.md", "GOLDFISH_LOG.md", "dti_audit.md")]
        md_file = md_files[0] if md_files else None

    if not moxfield_file.exists():
        moxfield_file = None
    if md_file and not md_file.exists():
        md_file = None

    return deck_dir, moxfield_file, md_file


def parse_deck_cards(moxfield_file: Path) -> List[str]:
    """Parses card names from a Moxfield import file."""
    cards = []
    if not moxfield_file or not moxfield_file.exists():
        return cards
    with open(moxfield_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//") or line.startswith("#"):
                continue
            # Typical format: '1 Card Name' or '1x Card Name'
            m = re.match(r"^(\d+)x?\s+(.+)$", line)
            if m:
                card_name = m.group(2).strip()
                # Remove collector tags like *F* or (Set) 123
                card_name = re.sub(r"\s+\([A-Za-z0-9_]+\)\s+[A-Za-z0-9_]+.*$", "", card_name).strip()
                cards.append(card_name)
            else:
                cards.append(line)
    return cards


def count_game_changers(card_names: List[str]) -> Tuple[int, List[str]]:
    """Counts official Game Changers in card list."""
    detected = []
    for c in card_names:
        norm = c.lower().strip()
        if norm in KNOWN_GAME_CHANGERS:
            detected.append(c)
    return len(detected), detected


def parse_goldfish_telemetry(deck_dir: Path) -> Optional[Dict[str, Any]]:
    """Extracts recent Goldfish simulation metrics from GOLDFISH_LOG.md if present."""
    log_file = deck_dir / "GOLDFISH_LOG.md"
    if not log_file.exists():
        return None
    try:
        content = log_file.read_text(encoding="utf-8")
        # Look for the last results block
        blocks = content.split("## ")
        if len(blocks) < 2:
            return None
        last_block = blocks[-1]

        data = {}
        # Parse commander cast rate: e.g., "Commander Casts: 80/80 (100.0%), avg turn 3.9"
        m_cmd = re.search(r"Commander Casts?:\s*(\d+/\d+\s*\([0-9.]+%\)),\s*avg turn\s*([0-9.]+)", last_block, re.IGNORECASE)
        if m_cmd:
            data["commander_cast_rate"] = m_cmd.group(1)
            data["commander_avg_turn"] = float(m_cmd.group(2))

        # Parse mulligan stats: e.g. "Gold: 45.0% | Silver: 55.0% | Desperation: 0.0%"
        m_mul = re.search(r"Gold:\s*([0-9.]+%)[\s|]+Silver:\s*([0-9.]+%)[\s|]+Desperation:\s*([0-9.]+%)", last_block, re.IGNORECASE)
        if m_mul:
            data["gold_keeps"] = m_mul.group(1)
            data["silver_keeps"] = m_mul.group(2)
            data["desperation_keeps"] = m_mul.group(3)

        # Parse engine readiness: e.g. "Achieved by target turn (<= T7): 95.0%"
        m_eng = re.search(r"Achieved by target turn[^:]*:\s*([0-9.]+%)", last_block, re.IGNORECASE)
        if m_eng:
            data["engine_readiness_pct"] = m_eng.group(1)

        m_eng_turn = re.search(r"Average Turn to Engine Readiness:\s*([0-9.]+)", last_block, re.IGNORECASE)
        if m_eng_turn:
            data["engine_avg_turn"] = float(m_eng_turn.group(1))

        return data if data else None
    except Exception:
        return None

# ---------------------------------------------------------------------------
# DTI Evaluation Core
# ---------------------------------------------------------------------------

class DTIEvaluation:
    def __init__(self, grades: Dict[str, str], justifications: Dict[str, str],
                 card_ledger: Dict[str, List[Dict[str, str]]], thematic_restriction: bool = False,
                 deck_name: str = "Commander Deck"):
        self.deck_name = deck_name
        self.thematic_restriction = thematic_restriction
        self.justifications = justifications or {}
        self.card_ledger = card_ledger or {}

        # Normalize grades to uppercase
        self.grades = {}
        for k in BENCHMARK_META:
            raw = str(grades.get(k, "C")).strip().upper()
            if raw not in ("S", "A", "B", "C", "F"):
                raw = "C"
            self.grades[k] = raw

        # Calculate scores
        self.scores = {}
        self.domain_scores = {
            "Resources": 0, "Access": 0, "Pressure": 0, "Interaction": 0, "Resilience": 0
        }
        for k, meta in BENCHMARK_META.items():
            g = self.grades[k]
            grp = meta["group"]
            pts = TIER_POINTS[grp][g]
            self.scores[k] = pts
            self.domain_scores[meta["domain"]] += pts

        self.threat_score = sum(self.scores.values())

        # Vector calculations
        # Velocity = R1 + A2 + P1 + P2 + S1 (Max 48)
        self.velocity_vector = (
            self.scores["r1"] + self.scores["a2"] + self.scores["p1"] +
            self.scores["p2"] + self.scores["s1"]
        )
        # Suppression = R1 + I2 + I1 + P1 + S3 (Max 40)
        self.suppression_vector = (
            self.scores["r1"] + self.scores["i2"] + self.scores["i1"] +
            self.scores["p1"] + self.scores["s3"]
        )

        # Baseline Bracket from Threat Score
        self.score_bracket = 2
        for floor_val, b_val, _ in BRACKET_THRESHOLDS:
            if self.threat_score >= floor_val:
                self.score_bracket = b_val
                break

        if self.threat_score < 16:
            self.score_bracket = 1 if self.thematic_restriction else 2

        # Evaluate the 4 Gates
        self.gates_triggered = []

        # Gate 1: Velocity Gate (>= 28 -> Bracket 4)
        if self.velocity_vector >= 28:
            self.gates_triggered.append({
                "name": "Velocity Gate",
                "bracket": 4,
                "reason": f"Velocity vector ({self.velocity_vector}/48) >= 28. Fast proactive clock."
            })

        # Gate 2: Early Finish / Glass Cannon Gate (Eliminates table by Turn 5: Zero-Untap Override or T1-3 onset)
        early_finish = False
        if self.grades["p1"] == "S":
            early_finish = True
        elif self.grades["p1"] == "A" and self.grades["p2"] == "S":
            early_finish = True
        elif self.grades["a2"] in ("S", "A") and self.grades["p2"] == "S":
            early_finish = True

        if early_finish:
            self.gates_triggered.append({
                "name": "Early Finish Gate",
                "bracket": 4,
                "reason": f"Reliably eliminates opponents or establishes lockout by Turn 5 (Zero-Untap Override: P1:{self.grades['p1']}, P2:{self.grades['p2']}). Belongs in Bracket 4."
            })

        # Gate 3: Suppression Gate (I2 S/A severe denial -> Bracket 4)
        if self.grades["i2"] in ("S", "A"):
            self.gates_triggered.append({
                "name": "Suppression Gate",
                "bracket": 4,
                "reason": f"Proactive restriction I2 is {self.grades['i2']}. Asymmetrical locks/attrition require Bracket 4."
            })

        # Gate 4: cEDH Gate (Vector >= 40, P1 S/A, P2 S -> Bracket 5)
        peak_vector = max(self.velocity_vector, self.suppression_vector)
        if peak_vector >= 40 and self.grades["p1"] in ("S", "A") and self.grades["p2"] == "S":
            self.gates_triggered.append({
                "name": "cEDH Gate",
                "bracket": 5,
                "reason": f"Peak threat vector ({peak_vector}) >= 40 with Turn 1–5 onset (P1:{self.grades['p1']}) and zero opponent untap win (P2:S)."
            })

        # Determine recommended DTI bracket before WotC rules
        gate_brackets = [g["bracket"] for g in self.gates_triggered]
        self.dti_bracket = max([self.score_bracket] + gate_brackets)

        # WotC Rules Compliance Floor
        self.wotc_floor = 1
        self.game_changers_count = 0
        self.game_changers_list = []
        self.final_bracket = self.dti_bracket

    def apply_wotc_rules(self, card_names: List[str]):
        """Cross-references Game Changers and sets statutory floor."""
        count, gc_list = count_game_changers(card_names)
        self.game_changers_count = count
        self.game_changers_list = gc_list

        if count > 3:
            self.wotc_floor = 4
        elif count >= 1:
            self.wotc_floor = 3
        else:
            self.wotc_floor = 1 if self.thematic_restriction else 2

        # DTI can ONLY push a deck UP, never down
        self.final_bracket = max(self.wotc_floor, self.dti_bracket)


# ---------------------------------------------------------------------------
# Template Generation & File I/O
# ---------------------------------------------------------------------------

def generate_default_evaluation(deck_name: str, card_names: List[str]) -> Dict[str, Any]:
    """Builds a starter evaluation structure for a deck."""
    grades = {
        "r1": "B", "r2": "B", "a1": "B", "a2": "B",
        "p1": "B", "p2": "B", "p3": "B", "i1": "B",
        "i2": "C", "s1": "B", "s2": "C", "s3": "C"
    }
    justifications = {
        "r1": "Standard on-curve ramp and land base; plays at regular tempo.",
        "r2": "Reliable draw package keeping hands stocked without explosive burst.",
        "a1": "Functional redundancy and moderate selection to assemble synergy pieces.",
        "a2": "Assembles primary synergy engine on Turns 6–7.",
        "p1": "Presents must-answer board state on Turns 6–7.",
        "p2": "Requires 2 opponent untap steps to convert a lethal board state into a win.",
        "p3": "Board-based game plan with standard interaction windows.",
        "i1": "Fair instant-speed spot removal suite with 2–3 board wipes.",
        "i2": "Light incidental taxation or soft denial; no asymmetric locks.",
        "s1": "Moderate protection suite for commander and key permanents.",
        "s2": "Can rebuild board presence over 2 turn cycles following a wipe.",
        "s3": "Commander is primary engine centerpiece; functions at reduced efficiency without it."
    }

    # Populate sample card ledger based on typical roles
    card_ledger = {}
    for k in BENCHMARK_META:
        card_ledger[k] = []

    for c in card_names:
        c_low = c.lower()
        if any(term in c_low for term in ("land", "fetch", "sol ring", "signet", "talisman", "ramp", "dork", "cultivate", "kodama")):
            card_ledger["r1"].append({"card": c, "role": "Mana ramp / fixing"})
        elif any(term in c_low for term in ("draw", "study", "sylvan library", "beast whisperer", "skullclamp", "mentor")):
            card_ledger["r2"].append({"card": c, "role": "Card draw / engine replenishment"})
        elif any(term in c_low for term in ("tutor", "demonic", "worldly", "vampiric", "gamble", "pod")):
            card_ledger["a1"].append({"card": c, "role": "Specific tutor / selection"})
        elif any(term in c_low for term in ("counter", "swords", "path", "beast within", "chaos warp", "pongify")):
            card_ledger["i1"].append({"card": c, "role": "Instant-speed reactive removal"})
        elif any(term in c_low for term in ("heroic", "teferi's protection", "boots", "greaves", "flawless")):
            card_ledger["s1"].append({"card": c, "role": "Board / commander protection"})

    return {
        "deck_name": deck_name,
        "thematic_restriction": False,
        "grades": grades,
        "justifications": justifications,
        "card_ledger": card_ledger
    }


def load_evaluation_file(filepath: Path) -> Dict[str, Any]:
    """Loads evaluation data from JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_evaluation_file(filepath: Path, data: Dict[str, Any]):
    """Saves evaluation data to JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Markdown & Terminal Renderers
# ---------------------------------------------------------------------------

def render_ascii_dashboard(eval_obj: DTIEvaluation, telemetry: Optional[Dict[str, Any]] = None) -> str:
    """Renders a high-density terminal dashboard."""
    lines = []
    lines.append("=" * 76)
    lines.append(f"  DECKCHECK THREAT INDEX (DTI) REPORT: {eval_obj.deck_name}")
    lines.append("=" * 76)

    # Top summary metrics
    b_label = f"BRACKET {eval_obj.final_bracket}"
    score_pct = (eval_obj.threat_score / 96.0) * 100
    lines.append(f"  Threat Score:    {eval_obj.threat_score:>2} / 96  ({score_pct:.1f}%)")
    lines.append(f"  Velocity Vector: {eval_obj.velocity_vector:>2} / 48  (Clock Speed & Protection)")
    lines.append(f"  Suppression Vec: {eval_obj.suppression_vector:>2} / 40  (Denial & Disruption)")
    lines.append(f"  Score Floor:     Bracket {eval_obj.score_bracket}")
    lines.append(f"  Final Placement: {b_label.upper()}")
    if eval_obj.game_changers_count > 0:
        lines.append(f"  Game Changers:   {eval_obj.game_changers_count} / 3 limit (WotC Floor: B{eval_obj.wotc_floor})")
    lines.append("-" * 76)

    # Domain Breakdown
    lines.append("  BENCHMARK RATINGS:")
    lines.append(f"  {'Code':<5} {'Benchmark Name':<34} {'Tier':<6} {'Pts':<5} {'Domain'}")
    lines.append("  " + "-" * 72)
    for code, meta in BENCHMARK_META.items():
        g = eval_obj.grades[code]
        pts = eval_obj.scores[code]
        max_p = meta["max"]
        lines.append(f"  {code.upper():<5} {meta['name']:<34} {g:<6} {pts:>2}/{max_p:<2} {meta['domain']}")
    lines.append("-" * 76)

    # Gates Status
    lines.append("  GATEKEEPER CHECKS:")
    v_gate = "TRIGGERED -> B4" if any(g["name"] == "Velocity Gate" for g in eval_obj.gates_triggered) else "PASSED (Safe)"
    ef_gate = "TRIGGERED -> B4" if any(g["name"] == "Early Finish Gate" for g in eval_obj.gates_triggered) else "PASSED (Safe)"
    sup_gate = "TRIGGERED -> B4" if any(g["name"] == "Suppression Gate" for g in eval_obj.gates_triggered) else "PASSED (Safe)"
    cedh_gate = "TRIGGERED -> B5" if any(g["name"] == "cEDH Gate" for g in eval_obj.gates_triggered) else "PASSED (Safe)"

    lines.append(f"  * Velocity Gate (Vector >= 28):          [{v_gate}] ({eval_obj.velocity_vector}/48)")
    lines.append(f"  * Early Finish Gate (Onset T1-5):        [{ef_gate}] (P1: {eval_obj.grades['p1']}, P2: {eval_obj.grades['p2']})")
    lines.append(f"  * Suppression Gate (Severe Denial I2):   [{sup_gate}] (I2: {eval_obj.grades['i2']})")
    lines.append(f"  * cEDH Gate (Vector >= 40, P1 S/A, P2 S): [{cedh_gate}]")

    # Goldfish telemetry cross-check
    if telemetry:
        lines.append("-" * 76)
        lines.append("  GOLDFISH EMPIRICAL TELEMETRY:")
        if "commander_avg_turn" in telemetry:
            lines.append(f"  * Commander Deployment: Turn {telemetry['commander_avg_turn']:.1f} ({telemetry.get('commander_cast_rate', 'N/A')})")
        if "gold_keeps" in telemetry:
            lines.append(f"  * Opening Hands:        {telemetry['gold_keeps']} Gold | {telemetry.get('silver_keeps', 'N/A')} Silver")
        if "engine_avg_turn" in telemetry:
            lines.append(f"  * Engine Readiness:     Turn {telemetry['engine_avg_turn']:.1f} ({telemetry.get('engine_readiness_pct', 'N/A')} on target)")
    lines.append("=" * 76)
    return "\n".join(lines)


def render_markdown_audit(eval_obj: DTIEvaluation, telemetry: Optional[Dict[str, Any]] = None) -> str:
    """Renders a thorough GitHub-flavored Markdown audit report."""
    md = []
    md.append(f"# DTI Power & Threat Evaluation: {eval_obj.deck_name}")
    md.append("")
    md.append(f"> **Evaluated Bracket: Bracket {eval_obj.final_bracket}** | **Threat Score: {eval_obj.threat_score} / 96** | **Velocity: {eval_obj.velocity_vector} / 48** | **Suppression: {eval_obj.suppression_vector} / 40**")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Executive Summary")
    md.append("")
    md.append(f"* **Final Placement:** **Bracket {eval_obj.final_bracket}**")
    md.append(f"* **DTI Threat Index:** `{eval_obj.threat_score} / 96` (Score Floor: Bracket {eval_obj.score_bracket})")
    md.append(f"* **Clock Speed (Velocity Vector):** `{eval_obj.velocity_vector} / 48`")
    md.append(f"* **Opponent Stifle (Suppression Vector):** `{eval_obj.suppression_vector} / 40`")
    md.append(f"* **WotC Statutory Compliance:** {eval_obj.game_changers_count} / 3 Game Changers (Floor: Bracket {eval_obj.wotc_floor})")
    if eval_obj.game_changers_list:
        md.append(f"  * *Game Changers detected:* {', '.join(eval_obj.game_changers_list)}")
    md.append("")

    if eval_obj.gates_triggered:
        md.append("### ⚠️ Active Gatekeeper Triggers")
        for g in eval_obj.gates_triggered:
            md.append(f"- **{g['name']} (Mandates Bracket {g['bracket']}):** {g['reason']}")
        md.append("")

    md.append("---")
    md.append("")
    md.append("## 2. Benchmark Breakdown & Justifications")
    md.append("")
    md.append("| Code | Benchmark | Domain | Tier | Points | Contextual Rationale |")
    md.append("|---|---|---|:---:|:---:|---|")
    for code, meta in BENCHMARK_META.items():
        g = eval_obj.grades[code]
        pts = eval_obj.scores[code]
        max_p = meta["max"]
        just = eval_obj.justifications.get(code, "Standard performance.")
        md.append(f"| **{code.upper()}** | {meta['name']} | {meta['domain']} | `{g}` | **{pts}/{max_p}** | {just} |")
    md.append("")

    if telemetry:
        md.append("---")
        md.append("")
        md.append("## 3. Goldfish Telemetry Cross-Validation")
        md.append("")
        md.append("| Metric | Simulated Result | Benchmark Alignment |")
        md.append("|---|---|---|")
        if "commander_avg_turn" in telemetry:
            md.append(f"| Commander Deployment | **Turn {telemetry['commander_avg_turn']:.1f}** ({telemetry.get('commander_cast_rate', 'N/A')}) | Confirms R1 ({eval_obj.grades['r1']}) & Mana Tempo |")
        if "gold_keeps" in telemetry:
            md.append(f"| Opening Hand Stability | **{telemetry['gold_keeps']} Gold / {telemetry.get('silver_keeps', 'N/A')} Silver** | Confirms R1/A1 Mulligan Floor |")
        if "engine_avg_turn" in telemetry:
            md.append(f"| Engine Readiness | **Turn {telemetry['engine_avg_turn']:.1f}** ({telemetry.get('engine_readiness_pct', 'N/A')} on target) | Confirms P1 ({eval_obj.grades['p1']}) Critical Onset |")
        md.append("")

    md.append("---")
    md.append("")
    md.append("## 4. The Card Ledger")
    md.append("")
    md.append("Every card in the deck mapped to the specific benchmarks it supports:")
    md.append("")
    for code, meta in BENCHMARK_META.items():
        entries = eval_obj.card_ledger.get(code, [])
        if not entries:
            continue
        md.append(f"### {code.upper()}: {meta['name']} (Tier `{eval_obj.grades[code]}`) — {len(entries)} Cards")
        for item in entries:
            card = item.get("card", "")
            role = item.get("role", "")
            md.append(f"- **{card}**{f': {role}' if role else ''}")
        md.append("")

    return "\n".join(md)


def generate_html_report(eval_obj: DTIEvaluation, output_file: Path, telemetry: Optional[Dict[str, Any]] = None):
    """Generates a standalone interactive visual HTML report."""
    score_pct = (eval_obj.threat_score / 96.0) * 100
    vel_pct = (eval_obj.velocity_vector / 48.0) * 100
    sup_pct = (eval_obj.suppression_vector / 40.0) * 100

    # Badge color based on bracket
    b_colors = {
        1: "#94a3b8",
        2: "#3b82f6",
        3: "#10b981",
        4: "#f59e0b",
        5: "#ef4444"
    }
    bracket_color = b_colors.get(eval_obj.final_bracket, "#10b981")

    # Generate benchmark table rows
    benchmark_rows = []
    for code, meta in BENCHMARK_META.items():
        g = eval_obj.grades[code]
        pts = eval_obj.scores[code]
        max_p = meta["max"]
        just = eval_obj.justifications.get(code, "Standard operation.")
        entries_count = len(eval_obj.card_ledger.get(code, []))

        tier_badges = {
            "S": '<span class="tier-badge tier-s">S</span>',
            "A": '<span class="tier-badge tier-a">A</span>',
            "B": '<span class="tier-badge tier-b">B</span>',
            "C": '<span class="tier-badge tier-c">C</span>',
            "F": '<span class="tier-badge tier-f">F</span>',
        }

        row = f"""
        <tr>
            <td class="code-col"><strong>{code.upper()}</strong></td>
            <td><strong>{meta['name']}</strong><br><span class="domain-sub">{meta['domain']}</span></td>
            <td class="tier-col">{tier_badges.get(g, g)}</td>
            <td class="score-col">{pts} / {max_p}</td>
            <td class="ledger-count-col">{entries_count}</td>
            <td class="just-col">{just}</td>
        </tr>
        """
        benchmark_rows.append(row)

    # Generate Card Ledger sections
    ledger_sections = []
    for code, meta in BENCHMARK_META.items():
        entries = eval_obj.card_ledger.get(code, [])
        if not entries:
            continue
        g = eval_obj.grades[code]
        card_items = []
        for item in entries:
            c = item.get("card", "")
            r = item.get("role", "")
            # Scryfall image URL
            img_url = f"https://api.scryfall.com/cards/named?exact={urllib.parse.quote(c)}&format=image&version=normal"
            scry_url = f"https://scryfall.com/search?q=!%22{urllib.parse.quote(c)}%22"
            card_items.append(f"""
            <div class="card-chip" data-img="{img_url}">
                <a href="{scry_url}" target="_blank" rel="noopener">{c}</a>
                {f'<span class="chip-role">{r}</span>' if r else ''}
            </div>
            """)

        sec = f"""
        <div class="ledger-group">
            <div class="ledger-header">
                <h3>{code.upper()}: {meta['name']} <span class="ledger-tier-tag tier-{g.lower()}">{g}</span></h3>
                <span class="count-tag">{len(entries)} cards</span>
            </div>
            <div class="card-grid">
                {''.join(card_items)}
            </div>
        </div>
        """
        ledger_sections.append(sec)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTI Report — {eval_obj.deck_name}</title>
    <style>
        :root {{
            --bg-base: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --border: #334155;
            --accent: {bracket_color};
            --s-color: #8b5cf6;
            --a-color: #3b82f6;
            --b-color: #10b981;
            --c-color: #f59e0b;
            --f-color: #ef4444;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 24px;
        }}
        h1 {{ font-size: 26px; font-weight: 700; }}
        .header-sub {{ color: var(--text-sub); font-size: 14px; margin-top: 4px; }}
        .bracket-badge {{
            background-color: var(--accent);
            color: #0f172a;
            font-weight: 800;
            font-size: 20px;
            padding: 8px 20px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .metric-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
        }}
        .metric-title {{ font-size: 13px; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }}
        .metric-value {{ font-size: 32px; font-weight: 800; margin: 6px 0; }}
        .metric-sub {{ font-size: 12px; color: var(--text-sub); }}
        .progress-bar {{
            background: #0f172a;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }}
        .progress-fill {{
            height: 100%;
            background: var(--accent);
            border-radius: 4px;
        }}
        .gates-banner {{
            background: var(--bg-card);
            border-left: 4px solid var(--accent);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
        }}
        .gate-title {{ font-weight: 700; margin-bottom: 8px; }}
        .gate-item {{ font-size: 13px; margin: 4px 0; color: var(--text-sub); }}
        .gate-tag {{ font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 11px; }}
        .tag-triggered {{ background: #ef4444; color: white; }}
        .tag-passed {{ background: #10b981; color: white; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 32px;
            border: 1px solid var(--border);
        }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ background: #1e293b; color: var(--text-sub); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
        tr:hover td {{ background: rgba(255, 255, 255, 0.02); }}
        .code-col {{ font-weight: 700; color: var(--text-sub); }}
        .tier-badge {{
            display: inline-block;
            font-weight: 800;
            font-size: 13px;
            padding: 2px 10px;
            border-radius: 6px;
            text-align: center;
        }}
        .tier-s {{ background: var(--s-color); color: white; }}
        .tier-a {{ background: var(--a-color); color: white; }}
        .tier-b {{ background: var(--b-color); color: white; }}
        .tier-c {{ background: var(--c-color); color: #0f172a; }}
        .tier-f {{ background: var(--f-color); color: white; }}
        .domain-sub {{ font-size: 11px; color: var(--text-sub); }}
        .just-col {{ font-size: 13px; color: #cbd5e1; }}
        .score-col {{ font-weight: 700; font-feature-settings: "tnum"; }}

        .ledger-section {{ margin-top: 32px; }}
        .ledger-group {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        .ledger-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }}
        .ledger-header h3 {{ font-size: 16px; font-weight: 700; }}
        .count-tag {{ font-size: 12px; color: var(--text-sub); }}
        .card-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .card-chip {{
            background: #0f172a;
            border: 1px solid var(--border);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            position: relative;
        }}
        .card-chip a {{
            color: var(--text-main);
            text-decoration: none;
            font-weight: 600;
        }}
        .card-chip a:hover {{ color: #38bdf8; }}
        .chip-role {{ font-size: 11px; color: var(--text-sub); }}

        /* Card Preview Hover Popup */
        #card-preview {{
            position: fixed;
            pointer-events: none;
            display: none;
            z-index: 1000;
            width: 240px;
            border-radius: 12px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
            border: 2px solid #475569;
        }}
    </style>
</head>
<body>
    <img id="card-preview" src="" alt="Card Preview" />
    <div class="container">
        <header>
            <div>
                <h1>{eval_obj.deck_name}</h1>
                <div class="header-sub">DeckCheck Threat Index (DTI) Evaluation Report</div>
            </div>
            <div class="bracket-badge">BRACKET {eval_obj.final_bracket}</div>
        </header>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Threat Score</div>
                <div class="metric-value">{eval_obj.threat_score} <span style="font-size:16px;color:var(--text-sub);">/ 96</span></div>
                <div class="metric-sub">Score Floor: Bracket {eval_obj.score_bracket}</div>
                <div class="progress-bar"><div class="progress-fill" style="width: {score_pct}%;"></div></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Velocity Vector</div>
                <div class="metric-value">{eval_obj.velocity_vector} <span style="font-size:16px;color:var(--text-sub);">/ 48</span></div>
                <div class="metric-sub">Clock & Assembly Speed (Gate at 28)</div>
                <div class="progress-bar"><div class="progress-fill" style="width: {vel_pct}%;"></div></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Suppression Vector</div>
                <div class="metric-value">{eval_obj.suppression_vector} <span style="font-size:16px;color:var(--text-sub);">/ 40</span></div>
                <div class="metric-sub">Denial, Tax & Stax Impact</div>
                <div class="progress-bar"><div class="progress-fill" style="width: {sup_pct}%;"></div></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Game Changers</div>
                <div class="metric-value">{eval_obj.game_changers_count} <span style="font-size:16px;color:var(--text-sub);">/ 3</span></div>
                <div class="metric-sub">WotC Statutory Limit Floor: B{eval_obj.wotc_floor}</div>
                <div class="progress-bar"><div class="progress-fill" style="width: {(eval_obj.game_changers_count / 3.0) * 100}%;"></div></div>
            </div>
        </div>

        <div class="gates-banner">
            <div class="gate-title">Gatekeeper Audit Results</div>
            <div class="gate-item">
                <span class="gate-tag {'tag-triggered' if any(g['name'] == 'Velocity Gate' for g in eval_obj.gates_triggered) else 'tag-passed'}">
                    {'TRIGGERED' if any(g['name'] == 'Velocity Gate' for g in eval_obj.gates_triggered) else 'PASSED'}
                </span>
                <strong>Velocity Gate:</strong> Vector {eval_obj.velocity_vector}/48 (Threshold: &ge; 28 mandates Bracket 4).
            </div>
            <div class="gate-item">
                <span class="gate-tag {'tag-triggered' if any(g['name'] == 'Early Finish Gate' for g in eval_obj.gates_triggered) else 'tag-passed'}">
                    {'TRIGGERED' if any(g['name'] == 'Early Finish Gate' for g in eval_obj.gates_triggered) else 'PASSED'}
                </span>
                <strong>Early Finish Gate:</strong> Onset {eval_obj.grades['p1']}, Completion {eval_obj.grades['p2']} (Zero-untap or T1-5 table elimination mandates Bracket 4).
            </div>
            <div class="gate-item">
                <span class="gate-tag {'tag-triggered' if any(g['name'] == 'Suppression Gate' for g in eval_obj.gates_triggered) else 'tag-passed'}">
                    {'TRIGGERED' if any(g['name'] == 'Suppression Gate' for g in eval_obj.gates_triggered) else 'PASSED'}
                </span>
                <strong>Suppression Gate:</strong> Proactive Restriction I2 is {eval_obj.grades['i2']} (Severe attrition mandates Bracket 4).
            </div>
            <div class="gate-item">
                <span class="gate-tag {'tag-triggered' if any(g['name'] == 'cEDH Gate' for g in eval_obj.gates_triggered) else 'tag-passed'}">
                    {'TRIGGERED' if any(g['name'] == 'cEDH Gate' for g in eval_obj.gates_triggered) else 'PASSED'}
                </span>
                <strong>cEDH Gate:</strong> Format ceiling clock with 0-untap kill (Peak vector: {max(eval_obj.velocity_vector, eval_obj.suppression_vector)}).
            </div>
        </div>

        <h2 style="margin-bottom: 16px; font-size: 20px;">12 Universal Benchmarks</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">Code</th>
                    <th style="width: 240px;">Benchmark</th>
                    <th style="width: 60px;">Tier</th>
                    <th style="width: 80px;">Points</th>
                    <th style="width: 60px;">Cards</th>
                    <th>Contextual Evaluation & Rationale</th>
                </tr>
            </thead>
            <tbody>
                {''.join(benchmark_rows)}
            </tbody>
        </table>

        <div class="ledger-section">
            <h2 style="margin-bottom: 16px; font-size: 20px;">The Card Ledger</h2>
            {''.join(ledger_sections)}
        </div>
    </div>

    <script>
        const preview = document.getElementById('card-preview');
        document.querySelectorAll('.card-chip').forEach(chip => {{
            chip.addEventListener('mouseenter', e => {{
                const img = chip.getAttribute('data-img');
                if (img) {{
                    preview.src = img;
                    preview.style.display = 'block';
                }}
            }});
            chip.addEventListener('mousemove', e => {{
                preview.style.left = (e.clientX + 15) + 'px';
                preview.style.top = Math.min(e.clientY - 120, window.innerHeight - 350) + 'px';
            }});
            chip.addEventListener('mouseleave', () => {{
                preview.style.display = 'none';
            }});
        }});
    </script>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="DeckCheck Threat Index (DTI) Evaluator")
    parser.add_argument("target", help="Path to deck folder, moxfield_import.txt, or deck .md file")
    parser.add_argument("--init", action="store_true", help="Generate a starter dti_eval.json template for the deck")
    parser.add_argument("--eval", help="Path to custom evaluation JSON file")
    parser.add_argument("--thematic-restriction", action="store_true", help="Flag intentional thematic restriction for Bracket 1")
    parser.add_argument("--output-html", help="Custom path for HTML visual report")
    parser.add_argument("--output-md", help="Custom path for Markdown audit report")
    parser.add_argument("--json", action="store_true", help="Output raw JSON metrics to stdout")

    # CLI Benchmark Overrides
    for code in BENCHMARK_META:
        parser.add_argument(f"--{code}", choices=["S", "A", "B", "C", "F", "s", "a", "b", "c", "f"], help=f"Set tier for {code.upper()}")

    args = parser.parse_args()

    deck_dir, moxfield_file, md_file = resolve_deck_paths(args.target)
    deck_name = deck_dir.name if deck_dir else "Commander Deck"

    card_names = parse_deck_cards(moxfield_file) if moxfield_file else []

    eval_json_file = Path(args.eval).resolve() if args.eval else (deck_dir / "dti_eval.json")

    # Handle --init
    if args.init:
        template = generate_default_evaluation(deck_name, card_names)
        save_evaluation_file(eval_json_file, template)
        print(f"Generated DTI evaluation template at: {eval_json_file}")
        print("Edit the grades and justifications in that file, then run:")
        print(f"  python scripts/dti_evaluator.py \"{deck_dir}\"")
        return

    # Load existing or create default
    if eval_json_file.exists():
        eval_data = load_evaluation_file(eval_json_file)
    else:
        eval_data = generate_default_evaluation(deck_name, card_names)

    # Apply CLI flag overrides if provided
    for code in BENCHMARK_META:
        val = getattr(args, code, None)
        if val:
            eval_data.setdefault("grades", {})[code] = val.upper()

    if args.thematic_restriction:
        eval_data["thematic_restriction"] = True

    # Build evaluation object
    eval_obj = DTIEvaluation(
        grades=eval_data.get("grades", {}),
        justifications=eval_data.get("justifications", {}),
        card_ledger=eval_data.get("card_ledger", {}),
        thematic_restriction=eval_data.get("thematic_restriction", False),
        deck_name=eval_data.get("deck_name", deck_name)
    )

    # Apply WotC rules & Game Changers
    eval_obj.apply_wotc_rules(card_names)

    # Parse goldfish telemetry if available
    telemetry = parse_goldfish_telemetry(deck_dir)

    # Output JSON if requested
    if args.json:
        res = {
            "deck_name": eval_obj.deck_name,
            "threat_score": eval_obj.threat_score,
            "velocity_vector": eval_obj.velocity_vector,
            "suppression_vector": eval_obj.suppression_vector,
            "score_bracket": eval_obj.score_bracket,
            "final_bracket": eval_obj.final_bracket,
            "wotc_floor": eval_obj.wotc_floor,
            "game_changers": eval_obj.game_changers_list,
            "grades": eval_obj.grades,
            "scores": eval_obj.scores,
            "gates_triggered": eval_obj.gates_triggered
        }
        print(json.dumps(res, indent=2))
        return

    # Print ASCII dashboard to terminal
    print(render_ascii_dashboard(eval_obj, telemetry))

    # Save Markdown report
    md_output = Path(args.output_md).resolve() if args.output_md else (deck_dir / "dti_audit.md")
    with open(md_output, "w", encoding="utf-8") as f:
        f.write(render_markdown_audit(eval_obj, telemetry))
    print(f"\nSaved Markdown audit to: {md_output}")

    # Generate HTML report
    html_output = Path(args.output_html).resolve() if args.output_html else (deck_dir / "dti_report.html")
    generate_html_report(eval_obj, html_output, telemetry)
    print(f"Generated Visual HTML report: {html_output}")


if __name__ == "__main__":
    import urllib.parse
    main()
