# Goldfish Simulation Log: Svella, Ice Shaper ("The Icy Forge")

## 2026-08-29 — Cream of the Crop Integration (20 sims, T10 turns, Bracket 3)

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

  Sim 1: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 3, 2]  |  Avg creatures: 3.0
  Sim 2: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 2, 8, 3]  |  Avg creatures: 3.2
  Sim 3: Commander cast 3/4  |  Earliest: T3    |  Turns: [3, 3, 3]     |  Avg creatures: 3.8
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 2, 3, 3]  |  Avg creatures: 3.8
  Sim 5: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 2, 2]  |  Avg creatures: 3.8
  Sim 6: Commander cast 4/4  |  Earliest: T2    |  Turns: [7, 4, 2, 3]  |  Avg creatures: 3.2
  Sim 7: Commander cast 4/4  |  Earliest: T1    |  Turns: [1, 3, 2, 3]  |  Avg creatures: 4.0
  Sim 8: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 2, 3, 3]  |  Avg creatures: 3.0
  Sim 9: Commander cast 4/4  |  Earliest: T1    |  Turns: [1, 3, 3, 3]  |  Avg creatures: 3.2
  Sim 10: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 4, 4, 2]  |  Avg creatures: 3.8
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 4]  |  Avg creatures: 4.2
  Sim 12: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 3, 3]  |  Avg creatures: 3.2
  Sim 13: Commander cast 4/4  |  Earliest: T1    |  Turns: [1, 3, 3, 3]  |  Avg creatures: 3.8
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [7, 5, 2, 2]  |  Avg creatures: 2.2
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 3, 2]  |  Avg creatures: 3.2
  Sim 16: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 2]  |  Avg creatures: 3.2
  Sim 17: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 3, 2]  |  Avg creatures: 4.2
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 2, 3]  |  Avg creatures: 3.0
  Sim 19: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 3, 3]  |  Avg creatures: 3.2
  Sim 20: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 2, 4]  |  Avg creatures: 3.5

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T8
  Commander Cast Avg:   T2.9
  Commander Cast Distribution:
    T 1: ### (3)
    T 2: ######################### (25)
    T 3: ###################################### (38)
    T 4: ######### (9)
    T 5: # (1)
    T 7: ## (2)
    T 8: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   32/80 (40%)
    Silver Keep (Mana + Curve):          47/80 (59%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.91 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 68/80 (85%)
  Engine Readiness Avg:  T4.8
  Engine Readiness Distribution:
    T 2: ### (3)
    T 3: ############# (13)
    T 4: ######################## (24)
    T 5: ################## (18)
    T 6: #### (4)
    T 7: ###### (6)
    T 8: ##### (5)
    T 9: # (1)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Turn 2.9 Commander Deployment:** 83% of games deploy Svella on Turn 1, 2, or 3.
- **Topdeck Synergy:** Cream of the Crop provides a 2-drop enchantment that stacks the library on every creature entry to guarantee Svella's 8-mana ability hits a game-ending bomb.

---

## 2026-08-25 — 6-Card Optimization Audit (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/SvellaIceShaper/moxfield_import.txt" --bracket 3 --sims 20 --turns 10 --html "commander_decks/Planning/SvellaIceShaper/goldfish_report.html"
```

**Results:**
```text
  Commander cast rate: 79/80 (99%) | Commander Cast Avg: T3.0
  Gold Keeps: 34/80 (42%) | Silver Keeps: 45/80 (56%) | Avg Hand Size: 6.91
  Target Window Readiness (T<=7): 69/80 (86%) | Engine Readiness Avg: T4.8
  Bracket Compliance: PASS (Bracket 3)
```
