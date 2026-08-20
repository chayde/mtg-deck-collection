# Goldfish Log — Mahadi, Emporium Master ("The Blood Market")

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
  Commander Cast Distribution:
    T 1: ### (3)
    T 2: ############################# (29)
    T 3: ############################# (29)
    T 4: ####### (7)
    T 5: ##### (5)
    T 6: ## (2)
    T 7: # (1)
    T 8: ## (2)
    T 9: ## (2)

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
  Engine Readiness Distribution:
    T 1: ## (2)
    T 2: #### (4)
    T 3: ################## (18)
    T 4: ######################## (24)
    T 5: ################ (16)
    T 6: ###### (6)
    T 7: #### (4)
    T 8: ## (2)
    T 9: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.3, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Initial Build Performance:** 62% Gold Keeps with exceptional consistency. 3-CMC Mahadi deploys on Turn 3.1 on average, generating 3–5 Treasures by Turn 4.3 to trigger artifact-drain pingers (**Mirkwood Bats**, **Mayhem Devil**, **Marionette Master**) or fire off massive X-spells (**Torment of Hailfire**, **Exsanguinate**).
