# Goldfish Simulation Log: Svella, Ice Shaper ("The Icy Forge")

## 2026-08-25 — 6-Card Optimization Audit (20 sims, T10 turns, Bracket 3)

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

  Sim 1: Commander cast 4/4  |  Earliest: T2    |  Turns: [5, 3, 3, 2]  |  Avg creatures: 3.0
  Sim 2: Commander cast 3/4  |  Earliest: T2    |  Turns: [3, 2, 3]  |  Avg creatures: 2.8
  Sim 3: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 3, 3]  |  Avg creatures: 3.0
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 4, 3]  |  Avg creatures: 2.8
  Sim 5: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 5, 5, 3]  |  Avg creatures: 3.2
  Sim 6: Commander cast 4/4  |  Earliest: T1    |  Turns: [4, 3, 3, 1]  |  Avg creatures: 3.2
  Sim 7: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 2]  |  Avg creatures: 3.2
  Sim 8: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 3, 3]  |  Avg creatures: 2.8
  Sim 9: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 3, 4]  |  Avg creatures: 3.2
  Sim 10: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 3, 9]  |  Avg creatures: 2.8
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 4, 3]  |  Avg creatures: 3.5
  Sim 12: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 4, 3]  |  Avg creatures: 3.5
  Sim 13: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 2, 2]  |  Avg creatures: 3.0
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 3]  |  Avg creatures: 2.5
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 3, 2]  |  Avg creatures: 3.8
  Sim 16: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 3, 3]  |  Avg creatures: 3.0
  Sim 17: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 2, 3, 2]  |  Avg creatures: 3.8
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 2, 2]  |  Avg creatures: 3.0
  Sim 19: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 9, 3, 3]  |  Avg creatures: 3.5
  Sim 20: Commander cast 4/4  |  Earliest: T2    |  Turns: [5, 4, 2, 3]  |  Avg creatures: 2.5

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.0
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ##################### (21)
    T 3: ############################################# (45)
    T 4: ###### (6)
    T 5: #### (4)
    T 9: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   34/80 (42%)
    Silver Keep (Mana + Curve):          45/80 (56%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.91 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 69/80 (86%)
  Engine Readiness Avg:  T4.8
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ############## (14)
    T 4: ############################# (29)
    T 5: ############### (15)
    T 6: ###### (6)
    T 7: ### (3)
    T 8: #### (4)
    T 9: ##### (5)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Improved Gold Keep Rate:** Gold Keeps improved significantly from 31% to **42%** (+11% boost), driven by the addition of *Castle Garenbrig* and *Saryth, the Viper's Fang*.
- **Commander Deployment Speed:** Average commander cast improved to **Turn 3.0** (with 83% of all casts happening on Turn 2 or 3).
- **Engine Readiness:** Maintained a strong **Turn 4.8 average**, well inside the Bracket 3 Target Window (T $\le$ 7).

---

## 2026-08-25 — Initial Build Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/SvellaIceShaper/moxfield_import.txt" --bracket 3 --sims 20 --turns 10 --html "commander_decks/Planning/SvellaIceShaper/goldfish_report.html"
```

**Results:**
```text
  Commander cast rate: 79/80 (99%) | Commander Cast Avg: T3.1
  Gold Keeps: 25/80 (31%) | Silver Keeps: 54/80 (68%) | Avg Hand Size: 6.95
  Target Window Readiness (T<=7): 72/80 (90%) | Engine Readiness Avg: T4.8
  Bracket Compliance: PASS (Bracket 3)
```
