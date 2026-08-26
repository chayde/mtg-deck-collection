# Goldfish Simulation Log: Svella, Ice Shaper ("The Icy Forge")

## 2026-08-25 — Initial Build Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/SvellaIceShaper/moxfield_import.txt" --bracket 3 --sims 20 --turns 10 --html "commander_decks/Planning/SvellaIceShaper/goldfish_report.html"
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Svella, Ice Shaper (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

  Sim 1: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 4, 3]  |  Avg creatures: 4.0
  Sim 2: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 3, 3]  |  Avg creatures: 2.2
  Sim 3: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 3]  |  Avg creatures: 3.5
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 2, 3]  |  Avg creatures: 3.8
  Sim 5: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 2, 2]  |  Avg creatures: 2.8
  Sim 6: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 3, 3]  |  Avg creatures: 3.8
  Sim 7: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 2, 3, 3]  |  Avg creatures: 3.8
  Sim 8: Commander cast 4/4  |  Earliest: T3    |  Turns: [5, 3, 3, 3]  |  Avg creatures: 3.8
  Sim 9: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 2, 4]  |  Avg creatures: 3.5
  Sim 10: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 3]  |  Avg creatures: 3.8
  Sim 11: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 10, 3]  |  Avg creatures: 4.2
  Sim 12: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 3]  |  Avg creatures: 2.5
  Sim 13: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 2, 3]  |  Avg creatures: 1.8
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [5, 3, 3, 2]  |  Avg creatures: 4.8
  Sim 15: Commander cast 4/4  |  Earliest: T1    |  Turns: [2, 1, 3, 4]  |  Avg creatures: 1.8
  Sim 16: Commander cast 3/4  |  Earliest: T2    |  Turns: [2, 3, 3]  |  Avg creatures: 2.5
  Sim 17: Commander cast 4/4  |  Earliest: T1    |  Turns: [9, 3, 8, 1]  |  Avg creatures: 3.0
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 2]  |  Avg creatures: 3.2
  Sim 19: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 3, 2]  |  Avg creatures: 3.8
  Sim 20: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 3, 3]  |  Avg creatures: 2.5

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T10
  Commander Cast Avg:   T3.1
  Commander Cast Distribution:
    T 1: ## (2)
    T 2: ##################### (21)
    T 3: ########################################## (42)
    T 4: ######### (9)
    T 5: ## (2)
    T 8: # (1)
    T 9: # (1)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   25/80 (31%)
    Silver Keep (Mana + Curve):          54/80 (68%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.95 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 72/80 (90%)
  Engine Readiness Avg:  T4.8
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ########### (11)
    T 4: ######################### (25)
    T 5: ####################### (23)
    T 6: ##### (5)
    T 7: ###### (6)
    T 9: ### (3)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Exceptional Commander Deployment:** Svella hits the battlefield on Turn 3.1 on average (99% cast rate across 80 seats, with 79% of casts occurring on Turn 2 or 3).
- **Mulligan Stability:** 99% functional keeps (31% Gold, 68% Silver, only 1% Desperation keep) with an average starting hand size of 6.95 cards.
- **Engine Readiness:** 90% of games reach engine readiness by Turn 7 or earlier (average T4.8), generating massive mana bases and early activations.
