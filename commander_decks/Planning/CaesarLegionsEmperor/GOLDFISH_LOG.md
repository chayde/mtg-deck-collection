# Goldfish Simulation Log: Caesar, Legion's Emperor

Simulation logs and performance validation across iterations for **Caesar, Legion's Emperor** ({1}{R}{W}{B}).

---

## 2026-09-10 — Initial Inception & Baseline Trial (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/CaesarLegionsEmperor/moxfield_import.txt" --bracket 3 --sims 20 --turns 10
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Caesar, Legion's Emperor (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

  Sim 1: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 2, 2, 4]  |  Avg creatures: 2.8
  Sim 2: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 6, 6, 2]  |  Avg creatures: 4.0
  Sim 3: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 5]  |  Avg creatures: 4.5
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 5, 4]  |  Avg creatures: 2.8
  Sim 5: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 3, 6]  |  Avg creatures: 3.2
  Sim 6: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 3]  |  Avg creatures: 2.5
  Sim 7: Commander cast 4/4  |  Earliest: T1    |  Turns: [3, 4, 3, 1]  |  Avg creatures: 4.5
  Sim 8: Commander cast 4/4  |  Earliest: T2    |  Turns: [6, 2, 4, 2]  |  Avg creatures: 3.8
  Sim 9: Commander cast 4/4  |  Earliest: T4    |  Turns: [4, 7, 5, 7]  |  Avg creatures: 3.8
  Sim 10: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 2, 2]  |  Avg creatures: 4.5
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 4, 3]  |  Avg creatures: 3.2
  Sim 12: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 5, 2, 3]  |  Avg creatures: 3.2
  Sim 13: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 4, 2]  |  Avg creatures: 2.5
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 4, 2, 3]  |  Avg creatures: 3.0
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 5, 2, 3]  |  Avg creatures: 4.0
  Sim 16: Commander cast 4/4  |  Earliest: T2    |  Turns: [8, 4, 3, 2]  |  Avg creatures: 3.5
  Sim 17: Commander cast 4/4  |  Earliest: T2    |  Turns: [8, 2, 3, 5]  |  Avg creatures: 4.5
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 2, 4]  |  Avg creatures: 2.2
  Sim 19: Commander cast 3/4  |  Earliest: T2    |  Turns: [2, 3, 3]  |  Avg creatures: 4.0
  Sim 20: Commander cast 4/4  |  Earliest: T1    |  Turns: [5, 3, 3, 1]  |  Avg creatures: 3.2

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T8
  Commander Cast Avg:   T3.5
  Commander Cast Distribution:
    T 1: ## (2)
    T 2: #################### (20)
    T 3: ######################### (25)
    T 4: ################# (17)
    T 5: ####### (7)
    T 6: #### (4)
    T 7: ## (2)
    T 8: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   38/80 (48%)
    Silver Keep (Mana + Curve):          39/80 (49%)
    Desperation Keep (Mulligan to <=5):   3/80 (4%)
    Average Starting Hand Size:          6.86 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 73/80 (91%)
  Engine Readiness Avg:  T4.4
  Engine Readiness Distribution:
    T 1: # (1)
    T 2: ####### (7)
    T 3: ################### (19)
    T 4: ################## (18)
    T 5: #################### (20)
    T 6: ##### (5)
    T 7: ### (3)
    T 8: #### (4)
    T 9: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
*   **Rapid Commander Deployment:** 99% overall cast rate with an average deployment turn of **T3.5**. In 59% of games (47/80), Caesar was on the battlefield on or before Turn 3.
*   **Rock-Solid Opening Quality:** 97% functional hands (48% Gold Keeps, 49% Silver Keeps), with only a 4% desperation mulligan rate and an average hand size of 6.86.
*   **Target Bracket Alignment:** Achieves Engine Readiness on average at **T4.4**, with 91% readiness within the target window (<= Turn 7), cleanly passing the Bracket 3 compliance check.
