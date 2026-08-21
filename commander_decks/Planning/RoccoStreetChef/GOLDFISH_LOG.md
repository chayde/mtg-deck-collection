# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

## [2026-08-20] — Initial Build Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_203125.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Rocco, Street Chef (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 76/80 (95%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.9
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ############ (12)
    T 3: ##################### (21)
    T 4: ##################### (21)
    T 5: ########## (10)
    T 6: #### (4)
    T 7: ### (3)
    T 8: ### (3)
    T 9: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   41/80 (51%)
    Silver Keep (Mana + Curve):          38/80 (48%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.91 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 70/80 (88%)
  Engine Readiness Avg:  T4.8
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ########### (11)
    T 4: ######################### (25)
    T 5: ####################### (23)
    T 6: ##### (5)
    T 7: ##### (5)
    T 8: #### (4)
    T 9: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
