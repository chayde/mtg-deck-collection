# Goldfish Simulation Log: Yidris, Maelstrom Wielder

## 2026-08-21 — Budget Land Optimization Run: 6 Pain Lands, Fabled Passage, Rogue's Passage, Reliquary Tower, Path of Ancestry (20 sims, T10 turns, Bracket 3)

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

  Sim 1: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 5, 4, 3]  |  Avg creatures: 2.5
  Sim 2: Commander cast 4/4  |  Earliest: T2    |  Turns: [7, 4, 2, 4]  |  Avg creatures: 3.0
  Sim 3: Commander cast 4/4  |  Earliest: T3    |  Turns: [6, 3, 4, 3]  |  Avg creatures: 3.8
  Sim 4: Commander cast 4/4  |  Earliest: T4    |  Turns: [4, 4, 4, 4]  |  Avg creatures: 2.8
  Sim 5: Commander cast 2/4  |  Earliest: T3    |  Turns: [4, 3]        |  Avg creatures: 2.2
  Sim 6: Commander cast 4/4  |  Earliest: T3    |  Turns: [5, 4, 5, 3]  |  Avg creatures: 3.0
  Sim 7: Commander cast 4/4  |  Earliest: T4    |  Turns: [4, 4, 4, 4]  |  Avg creatures: 2.2
  Sim 8: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 4, 4]  |  Avg creatures: 2.2
  Sim 9: Commander cast 3/4  |  Earliest: T2    |  Turns: [5, 2, 4]     |  Avg creatures: 1.8
  Sim 10: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 8, 5, 4]  |  Avg creatures: 3.8
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [10, 4, 4, 2] |  Avg creatures: 2.2
  Sim 12: Commander cast 4/4  |  Earliest: T1    |  Turns: [3, 8, 1, 3]  |  Avg creatures: 2.8
  Sim 13: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 2, 3, 7]  |  Avg creatures: 3.0
  Sim 14: Commander cast 4/4  |  Earliest: T3    |  Turns: [5, 3, 5, 3]  |  Avg creatures: 2.8
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 3, 3, 2]  |  Avg creatures: 2.2
  Sim 16: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 4, 4, 2]  |  Avg creatures: 3.5
  Sim 17: Commander cast 4/4  |  Earliest: T1    |  Turns: [5, 1, 4, 4]  |  Avg creatures: 2.5
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 3, 2, 3]  |  Avg creatures: 3.5
  Sim 19: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 3, 4]  |  Avg creatures: 3.8
  Sim 20: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 4]  |  Avg creatures: 2.8

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 77/80 (96%)
  Commander Cast Range: T1 - T10
  Commander Cast Avg:   T3.8
  Commander Cast Distribution:
    T 1: ## (2)
    T 2: ######## (8)
    T 3: ####################### (23)
    T 4: ############################## (30)
    T 5: ######## (8)
    T 6: # (1)
    T 7: ## (2)
    T 8: ## (2)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   34/80 (42%)
    Silver Keep (Mana + Curve):          46/80 (57%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          7.00 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.7
  Engine Readiness Distribution:
    T 2: ### (3)
    T 3: ######### (9)
    T 4: ############################ (28)
    T 5: ######################## (24)
    T 6: #### (4)
    T 7: ### (3)
    T 8: ### (3)
    T 9: ## (2)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.7, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Velocity & Consistency:** 96% commander deployment rate with an average cast turn of T3.8 (Range T1–T10).
- **Mulligan Quality:** 42% Gold keeps and 57% Silver keeps (**100% functional opening hands with 0% desperation keeps**) and an average starting hand size of 7.00 cards.
- **Engine Readiness:** 89% of seats achieve full engine readiness on or before Turn 7 (Average T4.7), aligning with the Bracket 3 expected window.
- **HTML Report:** Comprehensive dashboard written to `goldfish_report_20260821_194547.html`.

---

## 2026-08-21 — Finalized Weak-Slot Optimization Run: Lotus Bloom, An Offer You Can't Refuse, Ancient Cellarspawn, Laelia, Selvala (20 sims, T10 turns, Bracket 3)

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

  Sim 1: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 4, 3, 3]  |  Avg creatures: 4.0
  Sim 2: Commander cast 2/4  |  Earliest: T3    |  Turns: [3, 4]        |  Avg creatures: 1.5
  Sim 3: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 2]  |  Avg creatures: 2.8
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 9, 2, 4]  |  Avg creatures: 2.0
  Sim 5: Commander cast 2/4  |  Earliest: T3    |  Turns: [3, 6]        |  Avg creatures: 1.8
  Sim 6: Commander cast 4/4  |  Earliest: T4    |  Turns: [4, 5, 4, 6]  |  Avg creatures: 2.5
  Sim 7: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 4, 3]  |  Avg creatures: 1.5
  Sim 8: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 2, 2]  |  Avg creatures: 2.2
  Sim 9: Commander cast 3/4  |  Earliest: T2    |  Turns: [5, 2, 2]     |  Avg creatures: 1.8
  Sim 10: Commander cast 3/4  |  Earliest: T3    |  Turns: [3, 5, 8]     |  Avg creatures: 3.2
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [10, 3, 2, 3] |  Avg creatures: 4.2
  Sim 12: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 4, 4]  |  Avg creatures: 3.2
  Sim 13: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 7, 3]  |  Avg creatures: 3.0
  Sim 14: Commander cast 3/4  |  Earliest: T3    |  Turns: [3, 9, 4]     |  Avg creatures: 2.5
  Sim 15: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 3]  |  Avg creatures: 2.5
  Sim 16: Commander cast 4/4  |  Earliest: T3    |  Turns: [10, 3, 3, 6] |  Avg creatures: 4.0
  Sim 17: Commander cast 4/4  |  Earliest: T3    |  Turns: [5, 3, 3, 9]  |  Avg creatures: 2.5
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 4, 3]  |  Avg creatures: 2.8
  Sim 19: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 4, 7, 3]  |  Avg creatures: 3.0
  Sim 20: Commander cast 3/4  |  Earliest: T3    |  Turns: [3, 3, 3]     |  Avg creatures: 2.2

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 72/80 (90%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.9
  Commander Cast Distribution:
    T 2: ########### (11)
    T 3: ############################# (29)
    T 4: ################# (17)
    T 5: #### (4)
    T 6: ### (3)
    T 7: ## (2)
    T 8: # (1)
    T 9: ### (3)
    T10: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   45/80 (56%)
    Silver Keep (Mana + Curve):          35/80 (44%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.94 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 63/80 (79%)
  Engine Readiness Avg:  T4.7
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ################### (19)
    T 4: ####################### (23)
    T 5: ########### (11)
    T 6: ###### (6)
    T 7: ### (3)
    T 8: # (1)
    T 9: ### (3)
    T10: ### (3)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.7, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
