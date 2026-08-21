# Goldfish Log — Mahadi, Emporium Master ("The Blood Market")

## [2026-08-20] — Black Market Connections & Damnation Integration (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/MahadiEmporium/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/MahadiEmporium/goldfish_audit_20260820_201355.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Mahadi, Emporium Master (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.4
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ############################## (30)
    T 3: ###################### (22)
    T 4: ########### (11)
    T 5: ###### (6)
    T 6: ### (3)
    T 7: ### (3)
    T 8: # (1)
    T 9: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   45/80 (56%)
    Silver Keep (Mana + Curve):          33/80 (41%)
    Desperation Keep (Mulligan to <=5):   2/80 (2%)
    Average Starting Hand Size:          6.91 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.8
  Engine Readiness Distribution:
    T 2: #### (4)
    T 3: ############# (13)
    T 4: #################### (20)
    T 5: ##################### (21)
    T 6: ####### (7)
    T 7: ###### (6)
    T 8: ### (3)
    T 9: ## (2)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Integration of Black Market Connections & Damnation:** Swapped *Species Specialist* for *Black Market Connections* (3-mode main phase Treasure, Draw, & Token engine) and *Chandra's Ignition* for *Damnation* (4-mana unconditional wipe). Compliance status remains **PASS** for Bracket 3.

---

## [2026-08-20] — Ophiomancer & Grave Pact Integration (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/MahadiEmporium/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/MahadiEmporium/goldfish_audit_20260820_200155.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Mahadi, Emporium Master (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T10
  Commander Cast Avg:   T3.3
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   47/80 (59%)
    Silver Keep (Mana + Curve):          30/80 (38%)
    Desperation Keep (Mulligan to <=5):   3/80 (4%)
    Average Starting Hand Size:          6.90 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.7
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.7, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
