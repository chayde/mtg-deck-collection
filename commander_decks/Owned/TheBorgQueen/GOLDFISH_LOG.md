# Goldfish Validation Log — The Borg Queen

## [2026-11-14] — Out-of-the-Box Precon Baseline (20 sims, T10 turns, Bracket 2)

**Command:**
```
python scripts/multiplayer_goldfish.py "commander_decks/Owned/TheBorgQueen/moxfield_import.txt" --sims 20 --turns 10 --bracket 2 --html "commander_decks/Owned/TheBorgQueen/goldfish_report.html"
```

**Results:**
```
--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 69/80 (86%)
  Commander Cast Range: T4 - T10
  Commander Cast Avg:   T7.1
  Commander Cast Distribution:
    T 4: #### (4)
    T 5: ##### (5)
    T 6: ################### (19)
    T 7: ############### (15)
    T 8: ########### (11)
    T 9: ####### (7)
    T10: ######## (8)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   34/80 (42%)
    Silver Keep (Mana + Curve):          45/80 (56%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.92 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 2 (Core) — Target T9)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=9): 61/80 (76%)
  Engine Readiness Avg:  T7.1
  Engine Readiness Distribution:
    T 4: #### (4)
    T 5: ##### (5)
    T 6: ################### (19)
    T 7: ############### (15)
    T 8: ########### (11)
    T 9: ####### (7)
    T10: ######## (8)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 7.1, perfectly positioned to execute and threaten a win on Bracket 2 (Core)'s target (Turn 9+).
```

**Notes:**
*   **Commander Velocity Bottleneck:** **The Borg Queen** ({4}{W}{U}{B}, CMC 7) achieved an **86% cast rate (69/80 seats)** across 10 turns at an average deployment of **Turn 7.1**, with 11/80 seats failing to cast her by T10 due to mana/color stalls or tapped land tempo drag.
*   **Opening Hand Stability:** **42% Gold Keeps / 56% Silver Keeps / 1% Desperation Keeps** (6.92 average hand size). Solid basic curve stability for a precon, though heavy tapland density delays Turn 2–4 mana curves.
*   **Bracket 2 vs. Bracket 3 Gap:** While T7.1 readiness comfortably passes **Bracket 2 (Core, target T9)** at 76% T≤9 readiness, it will struggle at **Bracket 3 (Upgraded, target T7)** unless we trim taplands, replace slow 4-CMC rocks (*Stonespeaker Crystal*, *Reconnaissance Partition*) and **Skycloud Expanse** (filter land), and inject tighter 2-CMC mana rocks / Esper draw engines so The Borg Queen reliably lands Turn 5–6.
*   **Report:** Interactive breakdown generated at [`goldfish_report.html`](goldfish_report.html).

---

## 2026-11-14 — Phase 1 Bracket 3 Upgrade Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Owned/TheBorgQueen/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html "commander_decks/Owned/TheBorgQueen/goldfish_report.html"
```

**Results:**
```text
--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 67/80 (84%)
  Commander Cast Range: T3 - T10
  Commander Cast Avg:   T6.9
  Commander Cast Distribution:
    T 3: # (1)
    T 4: ## (2)
    T 5: ########## (10)
    T 6: ############# (13)
    T 7: ###################### (22)
    T 8: ########## (10)
    T 9: #### (4)
    T10: ##### (5)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   31/80 (39%)
    Silver Keep (Mana + Curve):          47/80 (59%)
    Desperation Keep (Mulligan to <=5):   2/80 (2%)
    Average Starting Hand Size:          6.89 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 48/80 (60%)
  Engine Readiness Avg:  T6.9
  Engine Readiness Distribution:
    T 3: # (1)
    T 4: ## (2)
    T 5: ########## (10)
    T 6: ############# (13)
    T 7: ###################### (22)
    T 8: ########## (10)
    T 9: #### (4)
    T10: ##### (5)

  [BRACKET COMPLIANCE CHECK] Status: NOTICE (Slow Engine Setup)
  Deck deploys its engine by T6.9 (behind schedule for a T7+ win target). Consider adding more low-CMC ramp or enablers.
```

**Notes:**
*   **Phase 1 Delta vs. Out-of-the-Box Precon Baseline:**
    *   Average Commander deployment improved from **T7.1 ➔ T6.9**, and earliest possible Commander turn dropped from T4 to **T3** (Sim 10 Seat 3 via **Sol Ring** + **Arcane Signet** + **Urza, Lord High Artificer**).
    *   **Bracket 3 Target Window Readiness (`T<=7`):** Rose from **43/80 (53.8%)** precon to **48/80 (60.0%)** after swapping in **Sea of Clouds**, **Fellwar Stone**, **Etherium Sculptor**, **Urza, Lord High Artificer**, and **Liberator, Urza's Battlethopter** while cutting 4-CMC rocks (*Stonespeaker Crystal*, *Reconnaissance Partition*) and **Skycloud Expanse**.
    *   **Opening Hand Stability:** **39% Gold Keeps / 59% Silver Keeps / 2% Desperation Keeps** (6.89 average hand size).
    *   **Remaining Diagnostic Bottleneck (Phase 2 Target):** The simulator still flags `[BRACKET COMPLIANCE CHECK] Status: NOTICE (Slow Engine Setup)` because **The Borg Queen** costs 7 mana ({4}{W}{U}{B}) and 12 conditional/enters-tapped lands remain from the precon mana base (e.g., *Arcane Sanctum*, *Evolving Wilds*, *Terramorphic Expanse*, *Contaminated Landscape*, *Fetid Pools*, *Irrigated Farmland*, *Shore Leave Planet*, *Umbral Expanse*, *Snarls*). Phase 2 land upgrades (Fetches, Shocks, remaining Battlebond/Slow lands) will push T≤7 deployment well past 70%.
*   **Report:** Interactive breakdown generated at [`goldfish_report.html`](goldfish_report.html).

