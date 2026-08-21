# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

## [2026-08-20] — Smothering Tithe & Deflecting Palm Integration (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_204620.html
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
  Commander cast rate: 73/80 (91%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T4.1
  Commander Cast Distribution:
    T 2: ######## (8)
    T 3: ################################ (32)
    T 4: ######### (9)
    T 5: ########## (10)
    T 6: ####### (7)
    T 7: ### (3)
    T 8: ## (2)
    T10: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   41/80 (51%)
    Silver Keep (Mana + Curve):          39/80 (49%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.99 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 64/80 (80%)
  Engine Readiness Avg:  T5.1
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ####### (7)
    T 4: ########################## (26)
    T 5: ################# (17)
    T 6: ####### (7)
    T 7: ###### (6)
    T 8: #### (4)
    T 9: ## (2)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 5.1, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Integration of Smothering Tithe & Deflecting Palm:** Added *Smothering Tithe* [Game Changer #1] and *Deflecting Palm* (instant damage reflection). *Treebeard, Gracious Host* retained as premier pillar. Compliance status remains **PASS** for Bracket 3.

---

## [2026-08-20] — Bilbo, Fellow Conspirator Integration (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_203925.html
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
  Commander cast rate: 74/80 (92%)
  Commander Cast Range: T1 - T10
  Commander Cast Avg:   T4.1
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   38/80 (48%)
    Silver Keep (Mana + Curve):          40/80 (50%)
    Desperation Keep (Mulligan to <=5):   2/80 (2%)
    Average Starting Hand Size:          6.89 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 64/80 (80%)
  Engine Readiness Avg:  T5.0
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 5.0, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
