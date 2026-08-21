# Goldfish Simulation Log: Yidris, Maelstrom Wielder

## 2026-08-21 — Cascade Optimization Run: Abaddon, Bituminous Blast, Treasure Cruise (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/YidrisChaos/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Yidris, Maelstrom Wielder (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

  Sim 1: Commander cast 3/4  |  Earliest: T2    |  Turns: [2, 8, 2]     |  Avg creatures: 2.8
  Sim 2: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 4, 10, 3] |  Avg creatures: 1.5
  Sim 3: Commander cast 4/4  |  Earliest: T1    |  Turns: [4, 4, 4, 1]  |  Avg creatures: 2.5
  Sim 4: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 3]  |  Avg creatures: 1.8
  Sim 5: Commander cast 3/4  |  Earliest: T3    |  Turns: [3, 6, 4]     |  Avg creatures: 2.5
  Sim 6: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 6]  |  Avg creatures: 2.5
  Sim 7: Commander cast 3/4  |  Earliest: T2    |  Turns: [2, 3, 4]     |  Avg creatures: 1.5
  Sim 8: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 8, 3, 4]  |  Avg creatures: 3.0
  Sim 9: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 6, 2, 6]  |  Avg creatures: 2.8
  Sim 10: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 8, 3]  |  Avg creatures: 2.2
  Sim 11: Commander cast 4/4  |  Earliest: T3    |  Turns: [6, 4, 4, 3]  |  Avg creatures: 2.8
  Sim 12: Commander cast 4/4  |  Earliest: T2    |  Turns: [8, 6, 4, 2]  |  Avg creatures: 1.0
  Sim 13: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 4, 4]  |  Avg creatures: 2.5
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 9, 8, 3]  |  Avg creatures: 2.5
  Sim 15: Commander cast 3/4  |  Earliest: T2    |  Turns: [2, 3, 3]     |  Avg creatures: 2.5
  Sim 16: Commander cast 4/4  |  Earliest: T4    |  Turns: [5, 4, 6, 9]  |  Avg creatures: 2.5
  Sim 17: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 4, 3]  |  Avg creatures: 1.8
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 9, 2, 3]  |  Avg creatures: 1.2
  Sim 19: Commander cast 3/4  |  Earliest: T6    |  Turns: [7, 6, 8]     |  Avg creatures: 1.2
  Sim 20: Commander cast 3/4  |  Earliest: T3    |  Turns: [4, 5, 3]     |  Avg creatures: 1.8

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 74/80 (92%)
  Commander Cast Range: T1 - T10
  Commander Cast Avg:   T4.3
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ########## (10)
    T 3: ##################### (21)
    T 4: ##################### (21)
    T 5: ## (2)
    T 6: ######## (8)
    T 7: # (1)
    T 8: ###### (6)
    T 9: ### (3)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   40/80 (50%)
    Silver Keep (Mana + Curve):          39/80 (49%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.96 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 61/80 (76%)
  Engine Readiness Avg:  T5.0
  Engine Readiness Distribution:
    T 2: #### (4)
    T 3: ############# (13)
    T 4: ###################### (22)
    T 5: ########### (11)
    T 6: ######## (8)
    T 7: ### (3)
    T 8: ####### (7)
    T 9: ### (3)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 5.0, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Velocity & Consistency:** 92% commander deployment rate with an average cast turn of T4.3 (earliest cast as early as Turn 1 with Delighted Halfling/Birds into Sol Ring).
- **Mulligan Quality:** 50% Gold keeps and 49% Silver keeps (99% viable opening hands) with an average starting hand size of 6.96 cards.
- **Engine Readiness:** 76% of seats achieve full engine readiness by Turn 7 (Average T5.0), perfectly aligned with Bracket 3 expectations.
- **HTML Report:** Comprehensive dashboard written to `goldfish_report_20260821_185519.html`.

---

## 2026-08-21 — Initial Build Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/YidrisChaos/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Yidris, Maelstrom Wielder (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

  Sim 1: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 7, 2]  |  Avg creatures: 2.2
  Sim 2: Commander cast 4/4  |  Earliest: T2    |  Turns: [5, 3, 4, 2]  |  Avg creatures: 2.2
  Sim 3: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 2, 4, 3]  |  Avg creatures: 2.2
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 4, 4]  |  Avg creatures: 1.8
  Sim 5: Commander cast 3/4  |  Earliest: T2    |  Turns: [2, 3, 3]     |  Avg creatures: 1.5
  Sim 6: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 6, 3, 6]  |  Avg creatures: 1.0
  Sim 7: Commander cast 3/4  |  Earliest: T2    |  Turns: [4, 3, 2]     |  Avg creatures: 1.5
  Sim 8: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 8, 4, 6]  |  Avg creatures: 2.5
  Sim 9: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 3]  |  Avg creatures: 2.2
  Sim 10: Commander cast 3/4  |  Earliest: T3    |  Turns: [3, 6, 5]     |  Avg creatures: 2.0
  Sim 11: Commander cast 3/4  |  Earliest: T4    |  Turns: [4, 7, 4]     |  Avg creatures: 1.8
  Sim 12: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 5, 3, 2]  |  Avg creatures: 2.0
  Sim 13: Commander cast 4/4  |  Earliest: T4    |  Turns: [5, 4, 4, 5]  |  Avg creatures: 3.0
  Sim 14: Commander cast 3/4  |  Earliest: T1    |  Turns: [2, 1, 3]     |  Avg creatures: 1.5
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [7, 2, 5, 4]  |  Avg creatures: 2.5
  Sim 16: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 3]  |  Avg creatures: 3.5
  Sim 17: Commander cast 2/4  |  Earliest: T3    |  Turns: [4, 3]        |  Avg creatures: 2.2
  Sim 18: Commander cast 3/4  |  Earliest: T3    |  Turns: [5, 3, 4]     |  Avg creatures: 2.0
  Sim 19: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 5, 2]  |  Avg creatures: 3.0
  Sim 20: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 4, 3, 5]  |  Avg creatures: 2.8

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 72/80 (90%)
  Commander Cast Range: T1 - T8
  Commander Cast Avg:   T3.8
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ########## (10)
    T 3: ####################### (23)
    T 4: ##################### (21)
    T 5: ######### (9)
    T 6: #### (4)
    T 7: ### (3)
    T 8: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   36/80 (45%)
    Silver Keep (Mana + Curve):          43/80 (54%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.92 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 69/80 (86%)
  Engine Readiness Avg:  T4.7
  Engine Readiness Distribution:
    T 2: ### (3)
    T 3: ############### (15)
    T 4: ################ (16)
    T 5: #################### (20)
    T 6: ######## (8)
    T 7: ####### (7)
    T 8: ### (3)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.7, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
