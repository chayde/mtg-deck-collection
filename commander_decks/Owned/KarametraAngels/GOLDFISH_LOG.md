# Goldfish Log — Karametra, God of Harvests (The Heavenly Host)

## [2026-08-20] — Bracket Audit Test (Bracket 4 Validated) (20 sims, T10 turns, Bracket 4)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Owned/KarametraAngels/moxfield_import.txt --sims 20 --turns 10 --bracket 4 --html commander_decks/Owned/KarametraAngels/goldfish_audit_20260820_180922.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Karametra, God of Harvests (CMC 5)  |  Target: Bracket 4 (Optimized) (Target T5)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.9
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ########## (10)
    T 3: ##################### (21)
    T 4: ############################## (30)
    T 5: ###### (6)
    T 6: ##### (5)
    T 7: ### (3)
    T 8: ## (2)
    T 9: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   48/80 (60%)
    Silver Keep (Mana + Curve):          32/80 (40%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.96 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 4 (Optimized) — Target T5)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=5): 68/80 (85%)
  Engine Readiness Avg:  T3.9
  Engine Readiness Distribution:
    T 2: ########## (10)
    T 3: ###################### (22)
    T 4: ############################## (30)
    T 5: ###### (6)
    T 6: ##### (5)
    T 7: ### (3)
    T 8: ## (2)
    T 9: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 3.9, perfectly positioned to execute and threaten a win on Bracket 4 (Optimized)'s target (Turn 5+).
```

**Notes:**
- **Validated Bracket 4 (Optimized) Position:** Contains **4 Game Changers** (*Smothering Tithe*, *Aura Shards*, *Teferi's Protection*, *Worldly Tutor*).
- **Ramp Velocity:** 5-CMC Karametra lands on Turn 3.9 on average due to 1-2 CMC dork/ramp density, rapidly snowballing lands and casting high-CMC Angel threats by Turn 5.
