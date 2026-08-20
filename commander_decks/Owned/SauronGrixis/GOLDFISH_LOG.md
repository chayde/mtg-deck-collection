# Goldfish Log — Sauron, the Dark Lord (Finalized Grixis Amass)

## [2026-08-20] — Bracket Audit Test (Bracket 3 Validated) (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Owned/SauronGrixis/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Owned/SauronGrixis/goldfish_audit_20260820_181830.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Sauron, the Dark Lord (CMC 6)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 77/80 (96%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T5.4
  Commander Cast Distribution:
    T 2: # (1)
    T 3: ########### (11)
    T 4: ################# (17)
    T 5: ################## (18)
    T 6: ########### (11)
    T 7: ####### (7)
    T 8: ###### (6)
    T 9: #### (4)
    T10: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   47/80 (59%)
    Silver Keep (Mana + Curve):          32/80 (40%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.95 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 65/80 (81%)
  Engine Readiness Avg:  T5.4
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ########### (11)
    T 4: ################# (17)
    T 5: ################## (18)
    T 6: ########### (11)
    T 7: ####### (7)
    T 8: ###### (6)
    T 9: #### (4)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 5.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Validated Bracket 3 (Upgraded) Position:** Contains **1 Game Changer** (*The One Ring*).
- **Deployment Velocity:** 6-CMC Sauron with Ward protection lands on Turn 5.4 on average, establishing the Ring-tempt discard-draw-4 engine to threaten wins on Turn 7+.
