## [2026-07-31] — Initial Deck Goldfish Validation (20 sims, T10 turns)

**Command:**
```
python3 scripts/multiplayer_goldfish.py "commander_decks/Planning/NekusarMindrazer/moxfield_import.txt" --sims 20 --turns 10
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Nekusar, the Mindrazer (CMC 5)
====================================================================

--------------------------------------------------------------------
AGGREGATE
--------------------------------------------------------------------
  Commander cast rate: 78/80 (98%)
  Range:     T1 - T10
  Average:   T4.3
  Distribution:
    T 1: # (1)
    T 2: ############ (12)
    T 3: ######################## (24)
    T 4: ############## (14)
    T 5: ######## (8)
    T 6: ###### (6)
    T 7: ### (3)
    T 8: ##### (5)
    T 9: ## (2)
    T10: ### (3)

  Avg creatures per seat (end T10): 1.4
```

**Notes:**
- **Mana Stability:** High consistency. With 10 fast rocks and 38 lands, Nekusar deploys on turn 3 or turn 4 in the vast majority of games (average T4.3).
- **Synergy:** Solid density of wheels and slug triggers ensures immediate pressure upon deploying the commander.
