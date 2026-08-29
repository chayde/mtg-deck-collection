# Goldfish Simulation Log: Sygg, River Cutthroat ("The Toll of the River")

This log tracks goldfish simulation validation runs for Sygg, River Cutthroat to monitor opening hand quality, mana curve stability, commander deployment turn, and Bracket 3 engine velocity.

---

## 2026-08-29 — Initial Deck Validation (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/SyggRiverCutthroat/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html "commander_decks/Planning/SyggRiverCutthroat/goldfish_report.html"
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Sygg, River Cutthroat (CMC 2)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 78/80 (98%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.4
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ########################### (27)
    T 3: ################## (18)
    T 4: ############## (14)
    T 5: ######### (9)
    T 6: ######## (8)
    T 9: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   40/80 (50%)
    Silver Keep (Mana + Curve):          40/80 (50%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.97 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 77/80 (96%)
  Engine Readiness Avg:  T4.1
  Engine Readiness Distribution:
    T 2: ##### (5)
    T 3: ######################## (24)
    T 4: ##################### (21)
    T 5: ############### (15)
    T 6: ############ (12)
    T 9: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.1, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Exceptional Hand Consistency:** 100% functional keep rate (50% Gold, 50% Silver) with 0% desperation keeps and 6.97 average starting hand size, powered by 45 lands + 1 MDFC and a robust 2-mana rock suite.
- **Fast Deployment:** Sygg (CMC 2) deploys on Turn 2 in over 33% of games and on Turn 3–4 across the vast majority of runs (T3.4 average).
- **Engine Pacing:** Engine readiness achieves 96% reliability before Turn 7 (averaging Turn 4.1), flawlessly aligning with Bracket 3 expectations.
