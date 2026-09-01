# Goldfish Simulation Log: Henzie "Toolbox" Torre

## 2026-08-31 — Bracket 3 Overhaul Validation (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 76/80 (95%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.9
  Commander Cast Distribution:
    T 2: ################ (16)
    T 3: ############################# (29)
    T 4: ########## (10)
    T 5: ########## (10)
    T 6: # (1)
    T 7: ##### (5)
    T 8: ## (2)
    T 9: ## (2)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   32/80 (40%)
    Silver Keep (Mana + Curve):          46/80 (57%)
    Desperation Keep (Mulligan to <=5):   2/80 (2%)
    Average Starting Hand Size:          6.90 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.6
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ############### (15)
    T 4: ############################## (30)
    T 5: ############## (14)
    T 6: ##### (5)
    T 7: ##### (5)
    T 8: ## (2)
    T 9: ## (2)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.6, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- High 1-drop dork density enabled frequent Turn 2 Henzie deployments and consistent Turn 3/4 Blitz cadence.
- 89% of simulated hands achieved full Engine Readiness on or before Turn 7 (average Turn 4.6), comfortably passing Bracket 3 compliance.
- 97% combined Gold and Silver opening hand keep rate with a 6.90 card average starting hand.
