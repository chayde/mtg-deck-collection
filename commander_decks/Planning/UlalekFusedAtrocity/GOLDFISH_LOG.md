# Goldfish Simulation Log: Ulalek, Fused Atrocity

## 2026-08-11 — Zero Game Changer Calibration (20 sims, 10 turns)

**Goal:** Validate mana stability and cast velocity after replacing 3 high-dollar Game Changers (Ancient Tomb, The One Ring, Cyclonic Rift) with Temple of the False God, Kozilek's Unsealing, and Raise the Palisade.

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

  Sim 1: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 4]  |  Avg creatures: 2.8
  Sim 2: Commander cast 4/4  |  Earliest: T3    |  Turns: [5, 5, 3, 3]  |  Avg creatures: 4.0
  Sim 3: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 5, 4]  |  Avg creatures: 4.0
  Sim 4: Commander cast 4/4  |  Earliest: T1    |  Turns: [1, 8, 4, 4]  |  Avg creatures: 3.8
  Sim 5: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 5, 5, 2]  |  Avg creatures: 2.8
  Sim 6: Commander cast 4/4  |  Earliest: T3    |  Turns: [5, 3, 4, 6]  |  Avg creatures: 3.8
  Sim 7: Commander cast 4/4  |  Earliest: T4    |  Turns: [4, 4, 4, 7]  |  Avg creatures: 3.8
  Sim 8: Commander cast 4/4  |  Earliest: T1    |  Turns: [3, 5, 4, 1]  |  Avg creatures: 2.5
  Sim 9: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 4, 4]  |  Avg creatures: 5.5
  Sim 10: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 5, 3]  |  Avg creatures: 3.2
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 5, 2, 3]  |  Avg creatures: 4.5
  Sim 12: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 3, 5, 4]  |  Avg creatures: 3.5
  Sim 13: Commander cast 4/4  |  Earliest: T3    |  Turns: [5, 3, 5, 3]  |  Avg creatures: 3.8
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 3, 3]  |  Avg creatures: 3.5
  Sim 15: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 7, 3]  |  Avg creatures: 2.5
  Sim 16: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 3, 3]  |  Avg creatures: 2.0
  Sim 17: Commander cast 4/4  |  Earliest: T3    |  Turns: [4, 3, 4, 3]  |  Avg creatures: 3.2
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 5, 2, 3]  |  Avg creatures: 3.2
  Sim 19: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 5, 5]  |  Avg creatures: 3.0
  Sim 20: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 4, 3, 2]  |  Avg creatures: 3.2

--------------------------------------------------------------------
AGGREGATE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Range:     T1 - T8
  Average:   T3.7
  Distribution:
    T 1: ## (2)
    T 2: ####### (7)
    T 3: ############################# (29)
    T 4: ####################### (23)
    T 5: ############### (15)
    T 6: # (1)
    T 7: ## (2)
    T 8: # (1)

  Avg creatures per seat (end T10): 3.4
```

**Notes:**
* **Zero Performance Loss:** Replacing Ancient Tomb, The One Ring, and Cyclonic Rift did not lower cast consistency (still 100% cast rate at **T3.7 average**).
* **Cost Efficiency:** Shaved ~$280 off acquisition costs while establishing a completely pure 0-Game-Changer Bracket 3 profile.
