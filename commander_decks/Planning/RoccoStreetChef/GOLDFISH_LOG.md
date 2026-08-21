# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

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
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ########## (10)
    T 3: ############################## (30)
    T 4: ########## (10)
    T 5: ######## (8)
    T 6: ####### (7)
    T 8: #### (4)
    T10: #### (4)

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

**Notes:**
- **Integration of Bilbo, Fellow Conspirator:** Swapped *Butterbur, Bree Innkeeper* for *Bilbo, Fellow Conspirator* ({2}{G} — *If you would create a Food token, instead create a Food token and a Treasure token*). Compliance status remains **PASS** for Bracket 3.

---

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
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
