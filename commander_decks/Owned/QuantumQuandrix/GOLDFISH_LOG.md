# Goldfish Log — Quantum Quandrix (Adrix and Nev, Twincasters)

## [2026-08-20] — Bracket Audit Test (Bracket 3 Reclassification Validated) (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Owned/QuantumQuandrix/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Owned/QuantumQuandrix/goldfish_audit_20260820_181541.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Adrix and Nev, Twincasters (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T2 - T9
  Commander Cast Avg:   T4.1
  Commander Cast Distribution:
    T 2: ########## (10)
    T 3: ############ (12)
    T 4: ######################################### (41)
    T 5: ######## (8)
    T 6: ## (2)
    T 7: ## (2)
    T 8: #### (4)
    T 9: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   25/80 (31%)
    Silver Keep (Mana + Curve):          55/80 (69%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.99 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 72/80 (90%)
  Engine Readiness Avg:  T4.7
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ################ (16)
    T 4: ##################### (21)
    T 5: ############################ (28)
    T 6: ##### (5)
    T 7: # (1)
    T 8: ##### (5)
    T 9: ### (3)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.7, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Reclassified to Bracket 3 (Upgraded):** Goldfish simulation confirmed that despite containing zero Game Changers, the deck's upgraded token doubling engine (*Adrix and Nev*, *Esix*, *Koma*, *Scute Swarm*, *Second Harvest*) deploys commander on T4.1 and establishes engine readiness on T4.7, operating as an upgraded Bracket 3 deck.
