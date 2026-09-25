# DeckCheck Threat Index (DTI) Framework & Evaluation Guide

> **Authoritative Specification:** This document establishes the DeckCheck Threat Index (DTI) framework within this repository. It serves as our objective, physics-based system for grading Commander decks, diagnosing power level imbalances, and enforcing Bracket integrity (Brackets 1–5).

---

## 1. Executive Summary & Core Philosophy

Traditional power-level grading systems (and earlier iterations like CRISPI) evaluated decks by measuring their **"distance from cEDH"**. This created severe blind spots: a casual deck running an asymmetric lockout or early haymaker (such as *Cruelclaw* dropping a Turn-4 *Portal to Phyrexia* or *Grave Pact* loops) was often graded near a stock precon simply because it lacked cEDH staples (free countermagic, fast mana, or Thassa's Oracle combos).

The **DeckCheck Threat Index (DTI)** replaces distance-from-cEDH with the **Physics of Magic**: an economic and initiative race governed by compounding returns, multiplayer friction, and turn clocks.

### The Three Foundational Axioms

1. **Cards are Contextual:** A card only matters for what it does to the resource ledger (mana, cards, life, turn cycles) and the game plan of that specific deck. *Demonic Tutor* in a casual dragon typal deck is not the same card as *Demonic Tutor* in a Thoracle combo deck.
2. **Zones and Life are Aliases:** The graveyard and exile are dead zones until an engine makes them available. Life is an expendable buffer, not a win-likelihood meter.
3. **The Turn Clock is a Multiplier:** Decks win either by **contracting their own clock** (speed, burst mana, compact combos) or by **dilating the table's clock** (stax, tax, asymmetric attrition).

---

## 2. The 5 Domains & 12 Universal Benchmarks

Every Commander deck operates across 5 functional domains, evaluated through 12 universal benchmarks:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DTI DOMAIN HIERARCHY                            │
├───────────────┬───────────────┬───────────────┬──────────────┬─────────┤
│   RESOURCES   │    ACCESS     │   PRESSURE    │ INTERACTION  │RESIL.   │
│  (The Fuel)   │ (The Engine)  │ (Winning Game)│ (Disruption) │(Defense)│
├───────────────┼───────────────┼───────────────┼──────────────┼─────────┤
│ R1: Mana Vel. │ A1: Selection │ P1: Onset     │ I1: Reactive │ S1: Pro.│
│ R2: Card Flow │ A2: Assembly  │ P2: Inevit.   │ I2: Denial   │ S2: Rec.│
│               │               │ P3: Exposure  │              │ S3: Ind.│
└───────────────┴───────────────┴───────────────┴──────────────┴─────────┘
```

### Domain 1: Resources (The Engine's Fuel)
*   **R1 (Mana Velocity & Sufficiency):** How well does the deck produce the volume, colors, and tempo of mana (or cost-reduction/mana cheating) required to execute its game plan on its intended curve?
*   **R2 (Card Flow & Replenishment):** How well does the deck generate sustained net card advantage to fuel its plan beyond the standard draw step?

### Domain 2: Access (Finding & Structuring the Plan)
*   **A1 (Selection & Functional Redundancy):** How effectively does the deck eliminate variance to access specific pieces, tutors, or interchangeable functional packages?
*   **A2 (Assembly Velocity):** How reliably and quickly does the primary win plan, infinite loop, or dominant engine become fully assembled and castable?

### Domain 3: Pressure (Winning the Game)
*   **P1 (Critical Onset & Lethality):** How quickly and consistently does this deck present a must-answer state (threat of imminent kill, total lockout, or lethal board)?
*   **P2 (Win Inevitability & Compactness):** Once initiated, how many opponent untap cycles occur before this deck achieves an inevitable kill or total lockout?
*   **P3 (Exposure & Predictability):** How narrow is the interaction window capable of stopping this deck's win, and how easily can the table anticipate it?

### Domain 4: Interaction (Disrupting Opponents)
*   **I1 (Reactive Disruption):** How efficiently and flexibly can the deck disrupt opposing spells, permanents, or attacks at instant speed?
*   **I2 (Proactive Restriction & Denial):** How effectively does the deck lock out, tax, or systematically strip opponents of resources while breaking parity?

### Domain 5: Resilience (Surviving to Win)
*   **S1 (Plan Shielding & Protection):** How reliably can the deck protect its critical spells, permanents, or win turns from disruption?
*   **S2 (Engine Recovery):** How well does the deck rebuild its board, mana, or engine after a major wipe or disruption?
*   **S3 (Independence & Backup Plans):** How well can the deck function and win if its commander or primary centerpiece is neutralized?

---

## 3. Tier Evaluation Rubric (S through F)

Each benchmark is assigned a qualitative tier based on deck context:

| Tier | Name | Meaning & In-Game Impact |
|---|---|---|
| **S** | **Decisive / Format Ceiling** | Flawlessly satisfies the plan. Creates unrecoverable resource disparity, immediate locks, or executes at format-ceiling speed. |
| **A** | **Compounding Advantage** | Generates recurring surplus, multi-card swings per turn cycle, or scaling engines that comfortably outpace the pod. |
| **B** | **Advantage / High Synergy** | Net positive on curve. Reliably meets the deck's demands without compounding out of control. |
| **C** | **Parity / Baseline** | Even trades, 1-for-1 exchanges, variance smoothing, or minimum baseline operation with tempo friction. |
| **F** | **Deficit / Impaired** | Net loss. Costs more than it returns, fails to support the curve, or is dead/uncastable. |

### Concrete Benchmark Evaluation Ladders

*   **P1 (Critical Onset Turn):**
    *   **S:** Threatens lethal/lockout on **Turns 1–3** (cEDH speeds).
    *   **A:** Threatens lethal/lockout on **Turns 4–5** (High-power / Optimized).
    *   **B:** Threatens lethal/lockout on **Turns 6–7** (Upgraded Casual / Bracket 3).
    *   **C:** Threatens lethal/lockout on **Turns 8–9** (Precon / Core / Bracket 2).
    *   **F:** Turn 10+ or lacks any decisive win condition (Bracket 1).
*   **P2 (Opponent Untap Steps to Complete Win):**
    *   **S:** **0 Opponent Untap Steps** (instant-speed kill, storm chain, same-turn infinite loop, untelegraphed haste blowout). Opponents get zero turns to untap and draw answers.
    *   **A:** **1 Opponent Untap Step** (telegraphed lethal board passing priority once, or 2-turn lethal swing).
    *   **B:** **2 Opponent Untap Steps** (requires 2 full turn cycles of attacks/attrition).
    *   **C:** **3 Opponent Untap Steps** (slow cumulative combat clock).
    *   **F:** **4+ Untap Steps** or indefinite chip damage.
*   **R1 (Mana Velocity):**
    *   **S:** 0–1 CMC positive mana rocks (*Mox Diamond*, *Sol Ring*, *Mana Vault*), rituals (*Dark Ritual*), and flawless untapped fixing. Plays 2–3 turns ahead of curve.
    *   **A:** High density of efficient 2-CMC ramp, explosive landramp/dorks, or massive mana doublers (*Cabal Coffers*, *Nykthos*, *Mana Echoes*). Consistently ahead of curve.
    *   **B:** Standard 2–3 CMC ramp (*Cultivate*, *Arcane Signet*, Talismans) with solid curve hitting land drops reliably.
    *   **C:** Tapland drag, 3–4 CMC ramp, color-fixing friction.
    *   **F:** High curve, missing land drops, no ramp, mana starvation.
*   **I2 (Proactive Restriction & Denial):**
    *   **S:** Asymmetric hard locks, severe stax pieces (*Drannith Magistrate*, *Winter Orb*, *Possibility Storm* locks), or repeatable devastating attrition (*Grave Pact* / *Portal to Phyrexia* locks) deployed early.
    *   **A:** Strong repeatable resource denial or taxing (*Smothering Tithe*, *Oppression*, persistent edict triggers, soft stax).
    *   **B:** Incidental taxing, graveyard hate permanents (*Dauthi Voidwalker*, *Rest in Peace*), or light targeted denial.
    *   **C:** Symmetrical minor friction or single-shot sorcery-speed removal.
    *   **F:** Zero proactive disruption or resource denial.

---

## 4. Benchmark Weighting & Scoring Model

In Commander, **initiative and the turn clock dominate passive insurance**. A deck that threatens a protected win on Turn 3 does not care about rebuilding after a board wipe. To reflect real physics, benchmarks are divided into three weighted tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        BENCHMARK POINT VALUES                          │
├───────────────────────────────┬────┬───┬───┬───┬───┬───────────────────┤
│ Group                         │ S  │ A │ B │ C │ F │ Max Contribution  │
├───────────────────────────────┼────┼───┼───┼───┼───┼───────────────────┤
│ Terminal Clock (R1, A2, P1, P2│ 10 │ 5 │ 2 │ 1 │ 0 │ 4 × 10 = 40 pts   │
│ Execution Modifiers (6)       │  8 │ 4 │ 2 │ 1 │ 0 │ 6 ×  8 = 48 pts   │
│   (R2, A1, P3, I1, I2, S1)    │    │   │   │   │   │                   │
│ Contingency Buffers (S2, S3)  │  4 │ 2 │ 1 │ 0 │ 0 │ 2 ×  4 =  8 pts   │
├───────────────────────────────┴────┴───┴───┴───┴───┼───────────────────┤
│ TOTAL MAXIMUM THREAT SCORE                         │ 96 Points         │
└────────────────────────────────────────────────────┴───────────────────┘
```

*Points roughly halve with each drop in tier because format-ceiling performance warps entire games.*

---

## 5. Threat Vectors

To detect specialized or "min-maxed" decks (e.g. glass cannon combos or oppressive attrition engines), the framework computes two composite vectors:

### 1. Velocity Vector (Max 48)
Measures the speed, consistency, and protection of the deck's proactive clock:
$$\text{Velocity} = R1 + A2 + P1 + P2 + S1$$
*Components:* Mana Velocity (10) + Assembly (10) + Critical Onset (10) + Win Inevitability (10) + Protection (8).

### 2. Suppression Vector (Max 40)
Measures how effectively the deck shuts down and dilates opposing clocks:
$$\text{Suppression} = R1 + I2 + I1 + P1 + S3$$
*Components:* Mana Velocity (10) + Proactive Denial (8) + Reactive Disruption (8) + Threat Onset (10) + Independence (4).

---

## 6. Calibrated Bracket Thresholds & Hard Gates

A deck's final bracket is determined by combining:
1. **WotC Bracket Guidelines (Floor):** Game Changers count, Mass Land Denial, and chaining extra turns define the statutory floor. **DTI can only push a deck UP, never down.**
2. **Overall Threat Score Thresholds:**
   * **Bracket 1 (Exhibition):** `< 16` *(Requires deliberate thematic restriction or self-imposed handicap)*
   * **Bracket 2 (Core / Precon):** `16 – 31`
   * **Bracket 3 (Upgraded Casual):** `32 – 51`
   * **Bracket 4 (Optimized):** `52 – 67`
   * **Bracket 5 (cEDH):** `68 – 96` *(Requires supported competitive construction)*
3. **The 4 Hard Gates (Mechanical Overrides):**
   * **The Velocity Gate ($\ge 28 \rightarrow$ Min Bracket 4):** Any deck with a Velocity Vector $\ge 28$ is promoted to Bracket 4 regardless of its total score. A clock this fast breaks casual tables.
   * **The Early Finish Gate (Glass Cannon $\rightarrow$ Min Bracket 4):** Any deck that reliably eliminates opponents or achieves a game-ending lockout by **Turn 5** ($P1 \in \{S, A\}$) is promoted to Bracket 4.
   * **The Suppression Gate (Oppression Quarantine $\rightarrow$ Min Bracket 4):** Any deck deploying severe asymmetric locks or recurring attrition ($I2 \in \{S, A\}$) operating in the early game (by **Turn 6**) is quarantined to Bracket 4. *This permanently solves the pubstomper trap (e.g. Portal to Phyrexia / Grave Pact engines hiding in Bracket 3).*
   * **The cEDH Gate ($\rightarrow$ Min Bracket 5):** If Peak Vector ($\text{Velocity}$ or $\text{Suppression}$) $\ge 40$, threat onset $P1 \in \{S, A\}$, and completion $P2 = S$ (0 opponent untap steps), the deck is promoted to Bracket 5 even if its aggregate score is under 68.

---

## 7. The Card Ledger

A score without evidence is merely an opinion. Every DTI evaluation must generate a **Card Ledger**: an exhaustive mapping of every card in the deck to the specific benchmarks it supports.

*   Cards can and should appear under multiple benchmarks if they perform multiple roles (e.g., *Esper Sentinel* feeds $R2$ for card draw, $I2$ for taxing opponents, and $A2$ if feeding creature density).
*   Lands and fixing appear under $R1$.
*   Tutors and cantrips appear under $A1$ and $A2$.
*   Free interaction and countermagic appear under $I1$ and $S1$.

The Card Ledger provides immediate diagnostic clarity: if a deck's $R2$ (Card Flow) comes back as a $C$, looking at the ledger immediately reveals that only 3 or 4 cards support card replenishment, giving the deck builder a direct roadmap for tuning.

---

## 8. Integration with Repo Workflow

When evaluating, tuning, or creating decks in this repository:

1. **Card Verification:** Use `scripts/scryfall_lookup.py` to verify all cards and Game Changer tags.
2. **Empirical Grounding:** Run `scripts/multiplayer_goldfish.py` to collect real turn-clock and engine readiness data.
3. **Contextual Evaluation:** Assign qualitative tiers ($S$–$F$) to all 12 benchmarks and construct the Card Ledger.
4. **Deterministic Audit:** Run `python scripts/dti_evaluator.py` to calculate the Threat Score, verify all 4 Gates, check against WotC baseline rules, and generate `dti_report.html`.
5. **Visual Swaps:** Use `python scripts/swap_matrix.py` to adjust cards if the deck violates its target bracket.
