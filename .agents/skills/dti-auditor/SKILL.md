---
name: dti-auditor
description: >-
  Audits and categorizes Commander decks into brackets (1-5) using the DeckCheck
  Threat Index (DTI) framework. MANDATORY whenever creating, categorizing,
  assigning, or tuning a deck to a specific bracket, calculating Velocity and
  Suppression threat vectors, verifying gatekeepers, assembling card ledgers,
  and generating visual DTI HTML reports.
---

# DeckCheck Threat Index (DTI) Deck Auditor

This skill provides the authoritative runbook for evaluating any Magic: The Gathering Commander deck using the **DeckCheck Threat Index (DTI)** framework.

Traditional power-level evaluation failed because it treated power as "distance from cEDH." DTI replaces this with the **Physics of Magic**: an initiative-driven economic race governed by compounding returns, multiplayer friction, and turn clocks.

---

## The 3 Foundational Axioms

1. **Cards are Contextual:** A card only matters for what it does to the resource ledger (mana, cards, life, turn cycles) and the game plan of that specific deck.
2. **Zones and Life are Aliases:** Graveyard and exile are usable resource pools until denied; life is an expendable buffer.
3. **The Turn Clock is a Multiplier:** Decks win either by contracting their own clock (speed/combo) or dilating the table's clock (stax/attrition).

---

## The 12 Universal Benchmarks (5 Domains)

*   **Resources (The Fuel):**
    *   `R1` — Mana Velocity & Sufficiency (Clock, Max 10 pts)
    *   `R2` — Card Flow & Replenishment (Modifier, Max 8 pts)
*   **Access (The Engine):**
    *   `A1` — Selection & Functional Redundancy (Modifier, Max 8 pts)
    *   `A2` — Assembly Velocity (Clock, Max 10 pts)
*   **Pressure (Winning the Game):**
    *   `P1` — Critical Onset & Lethality (Clock, Max 10 pts: S=T1–3, A=T4–5, B=T6–7, C=T8–9, F=T10+)
    *   `P2` — Win Inevitability & Compactness (Clock, Max 10 pts: S=0 untap steps, A=1, B=2, C=3, F=4+)
    *   `P3` — Exposure & Predictability (Modifier, Max 8 pts)
*   **Interaction (Disruption):**
    *   `I1` — Reactive Disruption (Modifier, Max 8 pts)
    *   `I2` — Proactive Restriction & Denial (Modifier, Max 8 pts: S=Asymmetric hard lock/severe early attrition)
*   **Resilience (Defense):**
    *   `S1` — Plan Shielding & Protection (Modifier, Max 8 pts)
    *   `S2` — Engine Recovery (Buffer, Max 4 pts)
    *   `S3` — Independence & Backup Plans (Buffer, Max 4 pts)

---

## Step-by-Step Audit Procedure

### Step 1: Ingest Deck Context & Telemetry
1. Open and read `<deck_dir>/moxfield_import.txt` and the main `.md` deck file to understand the commander, archetype, and key win lines.
2. Check for `<deck_dir>/GOLDFISH_LOG.md`. If a goldfish simulation has been logged, note:
   * **Average Commander Deployment Turn** (grounds `R1` mana tempo).
   * **Opening Hand Keep Stability** (% Gold vs Silver vs Desperation).
   * **Average Engine Readiness Turn** (directly grounds `P1` critical onset turn).

### Step 2: Evaluate the 12 Benchmarks & Assign Tiers
Consult [`DTI_FRAMEWORK.md`](../../../DTI_FRAMEWORK.md) for the exact ladder criteria. Assign a tier (**S, A, B, C, F**) to each benchmark:
* `S` — Format Ceiling / Decisive
* `A` — Compounding Advantage
* `B` — Advantage / High Synergy
* `C` — Parity / Baseline Operation
* `F` — Impaired / Deficit

### Step 3: Construct the Card Ledger
Map every card in the deck to the specific benchmarks it supports. Cards that perform multiple functions appear under multiple benchmarks (e.g. *Esper Sentinel* under `R2`, `I2`, and `A2`).

### Step 4: Write or Update `<deck_dir>/dti_eval.json`
Save the evaluation data matching this JSON schema:
```json
{
  "deck_name": "DeckName",
  "thematic_restriction": false,
  "grades": {
    "r1": "A", "r2": "B", "a1": "B", "a2": "A",
    "p1": "B", "p2": "A", "p3": "B", "i1": "C",
    "i2": "F", "s1": "A", "s2": "C", "s3": "C"
  },
  "justifications": {
    "r1": "High density of fast mana dorks and cost reducers.",
    ...
  },
  "card_ledger": {
    "r1": [{"card": "Sol Ring", "role": "Positive mana rock"}],
    ...
  }
}
```

### Step 5: Execute the Deterministic Engine
Run the evaluator script from the repository root:
```bash
python scripts/dti_evaluator.py "<deck_dir>"
```

### Step 6: Review the 4 Hard Gatekeepers & WotC Floor
Check the output report to ensure no gatekeeper was unintentionally tripped:
1. **Velocity Gate ($\text{Velocity} = R1 + A2 + P1 + P2 + S1 \ge 28$):** Mandates **Bracket 4** regardless of total score.
2. **Early Finish Gate ($P1 \in \{S, A\}$):** Threatens win/lockout by Turn 5 $\rightarrow$ Mandates **Bracket 4**.
3. **Suppression Gate ($I2 \in \{S, A\}$):** Deploys severe asymmetric denial/attrition by Turn 6 $\rightarrow$ Mandates **Bracket 4**.
4. **cEDH Gate (Peak Vector $\ge 40$, $P1 \in \{S, A\}$, $P2 = S$):** Mandates **Bracket 5**.
5. **WotC Floor:** Game Changers count (0 for B1–2, $\le 3$ for B3, unlimited for B4–5). *Remember: DTI only pushes UP, never down.*

### Step 7: Deliver the Results
Provide the user with:
* The Threat Index score (out of 96) and Final Bracket placement.
* The Velocity (clock speed) and Suppression (denial) vector scores.
* Gatekeeper audit status (passed or triggered).
* Direct links to [`<deck_dir>/dti_audit.md`](./) and the interactive visual dashboard [`<deck_dir>/dti_report.html`](./).
