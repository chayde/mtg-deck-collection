# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

## [2026-08-20] — Complete Budget Overhaul Audit (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_210310.html
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
  Commander Cast Range: T1 - T10
  Commander Cast Avg:   T3.4
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ###################### (22)
    T 3: ################################## (34)
    T 4: ########### (11)
    T 5: #### (4)
    T 6: # (1)
    T 7: # (1)
    T 8: #### (4)
    T 9: # (1)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   54/80 (68%)
    Silver Keep (Mana + Curve):          26/80 (32%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.96 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 74/80 (92%)
  Engine Readiness Avg:  T4.4
  Engine Readiness Distribution:
    T 2: ### (3)
    T 3: ############### (15)
    T 4: ##################################### (37)
    T 5: ############## (14)
    T 6: # (1)
    T 7: #### (4)
    T 8: #### (4)
    T 9: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **High-Cost Spells & Fetch Land Removal:** Replaced *Deflecting Swat* ($68) with *Bolt Bend* ($2.77), *The Ozolith* ($65) with *Kami of Whispered Hopes* ($2.49), and *Smothering Tithe* ($61) with *Tireless Provisioner* ($1.16). Replaced all 8 fetch lands ($195+) with Check Lands (*Clifftop Retreat*, *Rootbound Crag*, *Sunpetal Grove*), Pain Lands (*Battlefield Forge*, *Brushland*, *Karplusan Forest*), and Basics.
- **Impact:** Total deck price cut from **$723.52 to $366.03** (-50%). **Commander cast rate reached 100% (T3.4 avg)**, **Gold Keeps hit 67.5%**, and **Engine Readiness reached T4.4 (92.5% target window rate)**.

---

## [2026-08-20] — Land-Base & Mana Fixing Optimization (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_205030.html
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
  Commander Cast Avg:   T3.5
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   50/80 (62%)
    Silver Keep (Mana + Curve):          30/80 (38%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.97 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.3
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.3, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
