# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

## [2026-08-20] — Banquet Guests & Conclave Mentor Integration (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_211455.html
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
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.2
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ##################### (21)
    T 3: ##################################### (37)
    T 4: ######## (8)
    T 5: ###### (6)
    T 6: #### (4)
    T 7: # (1)
    T 9: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   53/80 (66%)
    Silver Keep (Mana + Curve):          27/80 (34%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.96 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 77/80 (96%)
  Engine Readiness Avg:  T4.3
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ################## (18)
    T 4: ############################### (31)
    T 5: #################### (20)
    T 6: ###### (6)
    T 7: # (1)
    T 8: # (1)
    T 9: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.3, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Integration of Banquet Guests & Conclave Mentor:** Removed *Lathiel, the Bounteous Dawn* and *Blossoming Bogbeast*. Added **Banquet Guests** ({X}{G}{W} — *Affinity for Foods, enters with double X counters*) and **Conclave Mentor** ({G}{W} — *+1 extra counter on all creature counter placements*).
- **Impact:** **Target window readiness hit 96.25% (T<=7)**, **Commander Cast Avg hit T3.2**, and **Gold Keeps reached 66%**.

---

## [2026-08-20] — Sub-$300 Budget Overhaul with Baylen, the Haymaker (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_211210.html
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
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T1 - T8
  Commander Cast Avg:   T3.1
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   43/80 (54%)
    Silver Keep (Mana + Curve):          37/80 (46%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.99 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 76/80 (95%)
  Engine Readiness Avg:  T4.2
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.2, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
