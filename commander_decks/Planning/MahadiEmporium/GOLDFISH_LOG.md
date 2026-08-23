# Goldfish Log — Mahadi, Emporium Master ("The Blood Market")

## [2026-08-22] — 100-Card Standard Alignment & Trim (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py commander_decks/Planning/MahadiEmporium/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/MahadiEmporium/goldfish_audit_20260822_234800.html
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
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T1 - T6
  Commander Cast Avg:   T2.9
  Commander Cast Distribution:
    T 1: ## (2)
    T 2: ##################### (21)
    T 3: ############################################## (46)
    T 4: ##### (5)
    T 5: #### (4)
    T 6: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   44/80 (55%)
    Silver Keep (Mana + Curve):          36/80 (45%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.94 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 77/80 (96%)
  Engine Readiness Avg:  T4.1
  Engine Readiness Distribution:
    T 1: # (1)
    T 2: ######## (8)
    T 3: ############## (14)
    T 4: ########################### (27)
    T 5: ##################### (21)
    T 6: ###### (6)
    T 8: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.1, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **100-Card Singleton Standard Alignment:** Trimmed 7 redundant cards (*Merciless Executioner*, *Lightning Bolt*, *Impact Tremors*, *Sifter of Skulls*, *Garna, Bloodfist of Keld*, *Demand Answers*, *Crackle with Power*) to bring deck from 107 to exactly 100 cards (1 Commander + 99 Main).
- **Performance Gains:** Commander cast rate reached **100% (80/80)** with average deployment moving up from T3.4 to **T2.9** (max T6 instead of T9). Target window readiness improved from 89% to **96% (77/80)**, and average engine readiness accelerated from T4.8 to **T4.1**. Desperation keeps dropped to **0%**. Bracket compliance status: **PASS**.

---

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
