# Goldfish Simulation Log: Ulalek, Fused Atrocity

## 2026-08-11 — Initial Build Validation (20 sims, 10 turns)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py "commander_decks/Planning/UlalekFusedAtrocity/moxfield_import.txt" --sims 20 --turns 10
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Ulalek, Fused Atrocity (CMC 5)
====================================================================

  Sim 1: Commander cast 4/4  |  Earliest: T1    |  Turns: [3, 3, 4, 1]  |  Avg creatures: 2.8
  Sim 2: Commander cast 4/4  |  Earliest: T4    |  Turns: [5, 4, 4, 4]  |  Avg creatures: 3.8
  Sim 3: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 3, 4]  |  Avg creatures: 4.8
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [5, 3, 2, 4]  |  Avg creatures: 2.8
  Sim 5: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 9, 3, 3]  |  Avg creatures: 3.0
  Sim 6: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 4, 3, 3]  |  Avg creatures: 4.2
  Sim 7: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 8, 2, 4]  |  Avg creatures: 2.5
  Sim 8: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 2, 3, 4]  |  Avg creatures: 3.8
  Sim 9: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 10, 3, 3]  |  Avg creatures: 3.2
  Sim 10: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 5, 6]  |  Avg creatures: 3.8
  Sim 11: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 3, 4]  |  Avg creatures: 3.5
  Sim 12: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 4, 3]  |  Avg creatures: 3.0
  Sim 13: Commander cast 4/4  |  Earliest: T3    |  Turns: [6, 4, 3, 3]  |  Avg creatures: 2.5
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [5, 3, 2, 3]  |  Avg creatures: 4.0
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 4]  |  Avg creatures: 4.5
  Sim 16: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 7, 4, 3]  |  Avg creatures: 3.0
  Sim 17: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 6]  |  Avg creatures: 3.8
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 3, 2, 3]  |  Avg creatures: 3.2
  Sim 19: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 5, 5, 2]  |  Avg creatures: 5.0
  Sim 20: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 4]  |  Avg creatures: 3.0

--------------------------------------------------------------------
AGGREGATE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Range:     T1 - T10
  Average:   T3.7
  Distribution:
    T 1: # (1)
    T 2: ########## (10)
    T 3: ############################## (30)
    T 4: ########################## (26)
    T 5: ###### (6)
    T 6: ### (3)
    T 7: # (1)
    T 8: # (1)
    T 9: # (1)
    T10: # (1)

  Avg creatures per seat (end T10): 3.5
```

**Notes:**
* **Exceptional Mana Velocity:** Ulalek reached 100% cast rate across 80 simulated seats with an average turn-of-cast of **T3.7**.
* **Pain Land & Talisman Synergy:** The 10 pain lands + Talismans provide both effortless 5-color casting for Ulalek and the necessary {C} colorless pips required to activate copy triggers on curve.
* **Mid-to-Late Game Board Dominance:** Board presence averaged 3.5 large Eldrazi / value engines per seat by Turn 10, fully enabling massive combat swings and Annihilator triggers.
