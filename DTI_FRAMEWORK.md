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
   * **The Early Finish Gate (Zero-Untap Override / Early Combo Finish $\rightarrow$ Min Bracket 4):** Promotes to Bracket 4 if a deck eliminates all opponents or establishes a game-ending lockout by **Turn 5** ($P1 = S$, or $P1/A2 \in \{S, A\}$ paired with $P2 = S$), OR if an Aggro-Combo deck achieves Turn 5 onset ($P1: A$) with 1 response cycle ($P2: A$) using compact infinite loops to close the game on Turn 5–6 (violating WotC Bracket 3's Turn 7 earliest win ceiling). Decks with Turn 5 onset that rely on fair combat damage without infinite combos (*TheHive*) afford interactive blocks and remain in Bracket 3.
   * **The Suppression Gate (Oppression Quarantine $\rightarrow$ Min Bracket 4):** Any deck deploying severe asymmetric locks or recurring attrition ($I2 \in \{S, A\}$) operating in the early game (by **Turn 6**) is quarantined to Bracket 4. *This permanently solves the pubstomper trap (e.g. Portal to Phyrexia, Grave Pact, or Maha/Massacre Wurm engines hiding in Bracket 3).*
   * **The cEDH Gate ($\rightarrow$ Min Bracket 5):** If Peak Vector ($\text{Velocity}$ or $\text{Suppression}$) $\ge 40$, threat onset $P1 \in \{S, A\}$, and completion $P2 = S$ (0 opponent untap steps), the deck is promoted to Bracket 5 even if its aggregate score is under 68.

---

## 7. The Full Audit & Narrative Schema

Every comprehensive DTI evaluation produces not just numeric scores, but a complete strategic diagnosis:

1. **Tactical Overview:** Narrative breakdown of the deck's turn-by-turn progression and core win condition.
2. **Operational Primer:**
   * **Core Strategy:** Numbered turn sequence (e.g. Turn 1–2 ramp $\rightarrow$ Turn 3–4 engine $\rightarrow$ Turn 5–6 kill).
   * **Mulligan Priorities:** Explicit "Keep" vs. "Avoid" opening hand criteria.
   * **Tactical Tips:** High-leverage sequencing, trigger stacking, and interaction timing.
3. **Strategic Weaknesses (Categorized Impact):**
   * 🔴 **Critical:** Plan-breaking vulnerabilities (e.g., rest-in-peace static graveyard hate, exile sweepers).
   * 🟡 **Moderate:** Friction points (e.g., Rule of Law stax, dork removal, instant-speed counterspells).
   * ⚪ **Minor:** Incidental friction (e.g., life loss from shocklands, pillowfort attack taxes).
4. **Key Engine Anchors:** Ranked list of the 12 most critical cards with their exact mechanical justifications.
5. **The Card Ledger:** An exhaustive mapping of every card in the 99 to the specific benchmarks it supports.

---

## 8. Calibrated Empirical Anchor Decks (Official DeckCheck Baselines)

These decks serve as our empirical calibration standard directly validated against DeckCheck's official web scanner:

| Metric | Anchor 1: TheHive (Slivers) | Anchor 2: HenzieBlitz (Jund Reanimator) | Anchor 3: RoccoStreetChef (Naya Food Midrange) | Anchor 4: Hearthhull (Jund Lands Precon) | Anchor 5: Y'shtola (Esper Spellslinger Precon) | Anchor 6: EtaliConqueror (Gruul ETB Stompy) | Anchor 7: IncredibleHulk (Temur Stompy & Combo) | Anchor 8: Karametra (Selesnya Angels & Landfall) | Anchor 9: Marchesa (Grixis Aristocrats & Loops) | Anchor 10: The Great Goblin (Rakdos Swarm & Aristocrats) | Anchor 11: Gisa the Hellraiser (Mono-Black Zombie Crimes) | Anchor 12: Krenko (Goblin Aggro-Combo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Archetype** | Sliver Tribal Aggro-Cascade | Jund Blitz Reanimator | Naya Food & Exile Midrange | Jund Lands & Aristocrats Precon | Esper Spellslinger Control Precon | Gruul Stompy / ETB Clone Ramp | Temur Stompy / +1/+1 Counters & Combat Combo | Selesnya Landfall / Angel Midrange | Grixis Aristocrats / +1/+1 Counter Reanimator | Rakdos Goblin Aristocrats | Mono-Black Zombie Typal / Crime Engine | Mono-Red Goblin Tribal Aggro-Combo |
| **Final Bracket** | **Bracket 3 (Upgraded Casual — Apex)** | **Bracket 4 (Optimized — Floor)** | **Bracket 3 (Upgraded Casual — Solid)** | **Bracket 3 (Upgraded Casual — Precon Floor)** | **Bracket 2 (Core / Precon — Apex Ceiling)** | **Bracket 3 (Upgraded Casual — Explosive Stompy)** | **Bracket 3 (Upgraded Casual — Exact Floor)** | **Bracket 3 (Upgraded Casual — Exact Floor)** | **Bracket 3 (Upgraded Casual — Solid)** | **Bracket 3 (Upgraded Casual — Solid)** | **Bracket 3 (Upgraded Casual — Game Changer Floor)** | **Bracket 4 (Optimized — WotC MLD Floor)** |
| **DTI Threat Score** | **50 / 96** (B3 band: 32–51) | **52 / 96** (B4 band: 52–67) | **46 / 96** (B3 band: 32–51) | **40 / 96** (B3 band: 32–51) | **31 / 96** (B2 band: 16–31) | **40 / 96** (B3 band: 32–51) | **32 / 96** (B3 band: 32–51) | **32 / 96** (B3 band: 32–51) | **37 / 96** (B3 band: 32–51) | **41 / 96** (B3 band: 32–51) | **31 / 96** (B2 band: 16–31; promoted to B3 via 3 Game Changers) | **42 / 96** (B3 band: 32–51; promoted to B4 via Blood Moon MLD) |
| **Velocity Vector** | **24 / 48** ($R1:5 + A2:5 + P1:5 + P2:5 + S1:4$) | **24 / 48** ($R1:5 + A2:10 + P1:5 + P2:2 + S1:2$) | **24 / 48** ($R1:5 + A2:10 + P1:5 + P2:2 + S1:2$) | **18 / 48** ($R1:5 + A2:5 + P1:2 + P2:5 + S1:1$) | **13 / 48** ($R1:2 + A2:5 + P1:2 + P2:2 + S1:2$) | **18 / 48** ($R1:5 + A2:5 + P1:5 + P2:2 + S1:1$) | **18 / 48** ($R1:5 + A2:5 + P1:5 + P2:2 + S1:1$) | **18 / 48** ($R1:5 + A2:5 + P1:2 + P2:2 + S1:4$) | **19 / 48** ($R1:5 + A2:5 + P1:2 + P2:5 + S1:2$) | **19 / 48** ($R1:5 + A2:5 + P1:2 + P2:5 + S1:2$) | **13 / 48** ($R1:2 + A2:5 + P1:2 + P2:2 + S1:2$) | **24 / 48** ($R1:5 + A2:5 + P1:5 + P2:5 + S1:4$) |
| **Suppression Vector** | **16 / 40** ($R1:5 + I2:2 + I1:2 + P1:5 + S3:2$) | **20 / 40** ($R1:5 + I2:4 + I1:4 + P1:5 + S3:2$) | **16 / 40** ($R1:5 + I2:0 + I1:4 + P1:5 + S3:2$) | **13 / 40** ($R1:5 + I2:2 + I1:2 + P1:2 + S3:2$) | **12 / 40** ($R1:2 + I2:2 + I1:4 + P1:2 + S3:2$) | **12 / 40** ($R1:5 + I2:0 + I1:1 + P1:5 + S3:1$) | **14 / 40** ($R1:5 + I2:0 + I1:2 + P1:5 + S3:2$) | **13 / 40** ($R1:5 + I2:2 + I1:2 + P1:2 + S3:2$) | **13 / 40** ($R1:5 + I2:2 + I1:2 + P1:2 + S3:2$) | **13 / 40** ($R1:5 + I2:2 + I1:2 + P1:2 + S3:2$) | **12 / 40** ($R1:2 + I2:2 + I1:4 + P1:2 + S3:2$) | **16 / 40** ($R1:5 + I2:2 + I1:2 + P1:5 + S3:2$) |
| **Engine Ready Turn** | Turn 4 ($A2: A$) | Turn 3 ($A2: S$) | Turn 3 ($A2: S$) | Turn 4 ($A2: A$) | Turn 4 ($A2: A$) | Turn 4 ($A2: A$) | Turn 5 ($A2: A$) | Turn 4 ($A2: A$) | Turn 4 ($A2: A$) | Turn 4 ($A2: A$) | Turn 4 ($A2: A$) | Turn 4 ($A2: A$) |
| **Threat Onset Turn** | Turn 5 ($P1: A$) | Turn 4 ($P1: A$) | Turn 5 ($P1: A$) | Turn 6 ($P1: B$) | Turn 7 ($P1: B$) | Turn 4 ($P1: A$) | Turn 5 ($P1: A$) | Turn 6 ($P1: B$) | Turn 6 ($P1: B$) | Turn 6 ($P1: B$) | Turn 6 ($P1: B$) | Turn 5 ($P1: A$) |
| **Untap Cycles ($P2$)** | 1 cycle ($P2: A$) $\rightarrow$ Turn 6 kill | 2 cycles ($P2: B$) $\rightarrow$ Turn 6 kill | 2 cycles ($P2: B$) $\rightarrow$ Turn 7 kill | 1 cycle ($P2: A$) $\rightarrow$ Turn 7 kill | 2 cycles ($P2: B$) $\rightarrow$ Turn 9 kill | 2 cycles ($P2: B$) $\rightarrow$ Turn 6 kill | 2 cycles ($P2: B$) $\rightarrow$ Turn 7 kill | 2 cycles ($P2: B$) $\rightarrow$ Turn 8 kill | 1 cycle ($P2: A$) $\rightarrow$ Turn 7 kill | 1 cycle ($P2: A$) $\rightarrow$ Turn 7 kill | 2 cycles ($P2: B$) $\rightarrow$ Turn 8 kill | 1 cycle ($P2: A$) $\rightarrow$ Turn 6 kill |
| **Key Benchmarks** | $R2: S, A1: S, A2: A, P1: A, I2: B$ | $R2: S, A2: S, P1: A, I1: A, I2: A$ | $R1: A, R2: S, A2: S, I1: A, I2: F, S2: S$ | $R1: A, R2: S, A1: A, A2: A, P1: B, P2: A, S1: C$ | $R1: B, R2: A, A1: B, A2: A, P1: B, P2: B, I1: A$ | $R1: A, R2: S, A1: S, A2: A, P1: A, P2: B, I1: C$ | $R1: A, R2: A, A1: B, A2: A, P1: A, P2: B, I1: B$ | $R1: A, R2: B, A2: A, P1: B, I2: B, S1: A, S2: A, S3: A$ | $R1: A, R2: A, A1: A, A2: A, P1: B, P2: A, I2: B, S2: A, S3: A$ | $R1: A, R2: S, A1: A, A2: A, P1: B, P2: A, I2: B, S2: A, S3: A$ | $R1: B, R2: A, A1: B, A2: A, P1: B, P2: B, I1: A, I2: B, S1: B, S2: A, S3: A$ | $R1: A, R2: A, A1: A, A2: A, P1: A, P2: A, P3: B, I1: B, I2: B, S1: A, S2: A, S3: A$ |
| **Calibration Principle** | High velocity and S-tier card flow with fair interaction and 1 untap step cap out at the B3 apex (50/96). | Asymmetric lock (*Maha* + board wipes) trips Suppression Gate ($I2: A$) straight to the B4 floor (52/96). | High engine speed ($A2: S$) and S-tier recovery ($S2: S$) sit safely in mid-B3 (46/96) due to zero stax/denial ($I2: F$) and 2 untap cycles. | Modern synergy precons land at 40/96: slower onset (Turn 6) and low shielding ($S1: C$), but S-tier card flow ($R2: S$) and high recursion ($S2: A$) comfortably exceed Bracket 2 (16–31). | Defines the exact ceiling of Bracket 2 (31/96): slower Turn 7 onset, 2 untap cycles ($P2: B$), and low velocity (13/48) cap out at 31 even with premier Esper control ($I1: A$). | Explosive Turn 4 onset ($P1: A$) remains in Bracket 3 (40/96) because concluding the game requires 2 untap cycles ($P2: B$, Turn 6 kill) and interaction is minimal ($I1: C, I2: F$). | Defines the exact floor of Bracket 3 (32/96): paired with Caltrops soft infinite combat loop, heavy green ramp and 8/8 trample onset establish the 32 threshold. | Re-confirms the exact 32/96 floor of Bracket 3 alongside Hulk: despite running 4 Game Changers and Aura Shards denial ($I2: B$), its Turn 4 engine, Turn 6 onset ($P1: B$), and 2 untap cycles anchor it firmly at 32/96. | Illustrates the impact of high compactness and redundancy: with 10 fast rocks ($R1: A$), high redundancy ($A1: A$), and infinite persist loops ($P2: A$), it finishes in 1 response cycle and lands squarely at 37/96 in mid-Bracket 3. | Demonstrates the power of S-tier card flow ($R2: S$) coupled with 1-cycle compactness ($P2: A$): continuous impulse draw off dying Goblins combined with the Putrid Goblin infinite persist loop lifts it cleanly to 41/96 in mid-Bracket 3. | Crucial empirical discovery confirming the statutory WotC Game Changer Floor ($DTI \ge \text{WotC Floor}$): while its physical clock and engine threat score is 31/96 (identical to Y'shtola at the apex ceiling of Bracket 2), running 3 official Game Changers (*Bolas's Citadel*, *Field of the Dead*, *The One Ring*) establishes a hard statutory floor of Bracket 3 (Upgraded Casual). | Crucial empirical discovery confirming DeckCheck's strict enforcement of WotC Mass Land Denial (MLD) rules: despite scoring 42/96 (solid Bracket 3) and running zero Game Changers (0/3) and zero 2-card combos, running Blood Moon (classified as Mass Land Denial) triggers a hard statutory floor of Bracket 4 (MLD not allowed in Bracket 3). Removing Blood Moon immediately returns the deck to Bracket 3 (Upgraded Casual). |

---

## 9. Integration with Repo Workflow

When evaluating, tuning, or creating decks in this repository:

1. **Card Verification:** Use `scripts/scryfall_lookup.py` to verify all cards and Game Changer tags.
2. **Empirical Grounding:** Run `scripts/multiplayer_goldfish.py` to collect real turn-clock and engine readiness data.
3. **Contextual Evaluation:** Assign qualitative tiers ($S$–$F$) to all 12 benchmarks, map the Card Ledger, and formulate the primer/weaknesses schema.
4. **Deterministic Audit:** Run `python scripts/dti_evaluator.py "<deck_dir>"` to calculate the Threat Score, verify all 4 Gates, check against WotC baseline rules, and generate `dti_report.html`.
5. **Visual Swaps:** Use `python scripts/swap_matrix.py` to adjust cards if the deck violates its target bracket.
