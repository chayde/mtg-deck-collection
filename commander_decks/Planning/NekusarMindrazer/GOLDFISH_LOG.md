## [2026-07-31] — Playtested Build Goldfish Validation (20 sims, T10 turns)

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
  Commander cast rate: 79/80 (99%)
  Range:     T1 - T10
  Average:   T4.4
  Distribution:
    T 1: # (1)
    T 2: ######### (9)
    T 3: ################# (17)
    T 4: ################### (19)
    T 5: #################### (20)
    T 6: #### (4)
    T 7: #### (4)
    T 8: # (1)
    T 9: ## (2)
    T10: ## (2)

  Avg creatures per seat (end T10): 2.7
```

**Notes:**
- **Outstanding Consistency:** 99% commander cast rate across 80 seats. Nekusar hits the board by T3-T4 in over 70% of games.
- **Creature Presence:** Average creature count increased to 2.7 (up from 1.4 in draft) thanks to *Ghyrson Starn*, *Harmonic Prodigy*, *The Locust God*, *Razorkin Needlehead*, *Scrawling Crawler*, *Nightscape Familiar*, and *Stormfist Crusader*.

---

## [2026-07-31] — Initial AI Draft Goldfish Validation (20 sims, T10 turns)

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
    T10: ## (2)

  Avg creatures per seat (end T10): 1.4
```
