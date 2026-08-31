# Goldfish Simulation Log: Felothar the Steadfast ("The Iron Citadel")

This log tracks goldfish simulation validation runs for Felothar the Steadfast to monitor opening hand quality, mana curve stability, commander deployment turn, and Bracket 3 engine velocity.

---

## 2026-08-31 — Initial Deck Validation (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/FelotharSteadfast/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html "commander_decks/Planning/FelotharSteadfast/goldfish_report.html"
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Felothar the Steadfast (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

  Sim 1: Commander cast 3/4  |  Earliest: T2    |  Turns: [4, 2, 2]  |  Avg creatures: 4.8
  Sim 2: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 2, 4, 3]  |  Avg creatures: 3.5
  Sim 3: Commander cast 4/4  |  Earliest: T4    |  Turns: [9, 8, 4, 4]  |  Avg creatures: 4.0
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 2, 5]  |  Avg creatures: 4.8
  Sim 5: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 3, 2, 4]  |  Avg creatures: 5.2
  Sim 6: Commander cast 2/4  |  Earliest: T3    |  Turns: [3, 5]  |  Avg creatures: 4.8
  Sim 7: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 2, 7, 3]  |  Avg creatures: 4.8
  Sim 8: Commander cast 4/4  |  Earliest: T3    |  Turns: [7, 4, 3, 4]  |  Avg creatures: 4.8
  Sim 9: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 2, 4, 6]  |  Avg creatures: 5.2
  Sim 10: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 4, 3]  |  Avg creatures: 4.0
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 7, 4, 4]  |  Avg creatures: 5.2
  Sim 12: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 2, 4]  |  Avg creatures: 3.8
  Sim 13: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 4]  |  Avg creatures: 4.5
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 3, 2, 2]  |  Avg creatures: 3.0
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 2, 2]  |  Avg creatures: 6.5
  Sim 16: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 4, 3]  |  Avg creatures: 3.8
  Sim 17: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 8, 4, 2]  |  Avg creatures: 4.8
  Sim 18: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 4, 3, 4]  |  Avg creatures: 5.0
  Sim 19: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 4]  |  Avg creatures: 3.0
  Sim 20: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 7, 4]  |  Avg creatures: 4.5

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 77/80 (96%)
  Commander Cast Range: T2 - T9
  Commander Cast Avg:   T3.6
  Commander Cast Distribution:
    T 2: ###################### (22)
    T 3: ################ (16)
    T 4: ############################# (29)
    T 5: ## (2)
    T 6: # (1)
    T 7: #### (4)
    T 8: ## (2)
    T 9: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   37/80 (46%)
    Silver Keep (Mana + Curve):          42/80 (52%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.96 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 72/80 (90%)
  Engine Readiness Avg:  T4.3
  Engine Readiness Distribution:
    T 2: ####### (7)
    T 3: ##################### (21)
    T 4: ##################### (21)
    T 5: ################## (18)
    T 6: # (1)
    T 7: #### (4)
    T 8: ### (3)
    T 9: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.3, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **High Consistency & Speed:** 96% Commander cast rate (avg T3.6) and 90% T$\le$7 engine readiness (avg T4.3), driven by the 2-mana defender ramp core (*Overgrown Battlement*, *Wall of Roots*, *Axebane Guardian*) and low-mana rocks.
- **Hand Quality:** 98% functional keeps (46% Gold, 52% Silver) with 6.96 average starting hand size.
- **Board Presence:** Averages 4.5+ high-toughness creatures in play by Turn 10, establishing a wall fortress ready for team vigilance combat and overrun burst.
