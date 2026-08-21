# Goldfish Log — Mahadi, Emporium Master ("The Blood Market")

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
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ############################ (28)
    T 3: ############################### (31)
    T 4: ###### (6)
    T 5: ######## (8)
    T 7: ## (2)
    T 9: # (1)
    T10: ## (2)

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
  Engine Readiness Distribution:
    T 1: # (1)
    T 2: ## (2)
    T 3: ################ (16)
    T 4: ################### (19)
    T 5: ######################### (25)
    T 6: ### (3)
    T 7: ##### (5)
    T 8: ## (2)
    T 9: ## (2)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.7, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Integration of Ophiomancer & Grave Pact:** Swapped *Zoyowa Lava-Tongue* for *Ophiomancer* (4 Deathtouch snakes per turn cycle) and *Judith* for *Grave Pact* (forced 3-player edict on every creature death). Performance remains **PASS** for Bracket 3.

---

## [2026-08-20] — Initial Build Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/MahadiEmporium/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/MahadiEmporium/goldfish_audit_20260820_195445.html
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
  Commander Cast Avg:   T3.1
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   50/80 (62%)
    Silver Keep (Mana + Curve):          29/80 (36%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.95 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 74/80 (92%)
  Engine Readiness Avg:  T4.3
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.3, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
