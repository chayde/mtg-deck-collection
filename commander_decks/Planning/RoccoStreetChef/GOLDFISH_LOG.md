# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

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
  Commander Cast Distribution:
    T 1: ## (2)
    T 2: ################### (19)
    T 3: ############################# (29)
    T 4: ########### (11)
    T 5: ###### (6)
    T 6: #### (4)
    T 7: # (1)
    T 8: ### (3)
    T 9: # (1)

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
  Engine Readiness Distribution:
    T 2: ##### (5)
    T 3: ################# (17)
    T 4: ############################## (30)
    T 5: ############# (13)
    T 6: ##### (5)
    T 7: # (1)
    T 8: ### (3)
    T 9: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.3, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Land-Base Overhaul:** Removed slow/tap lands (*Myriad Landscape*, *Path of Ancestry*, *Rockfall Vale*, *Overgrown Farmland*, *Sundown Pass*, *Kessig Wolf Run*). Added **City of Brass**, **Mana Confluence**, **Plaza of Heroes** (commander fixing + hexproof/indestructible protection), and Fast Lands (**Copperline Gorge**, **Razorverge Thicket**, **Inspiring Vantage**).
- **Impact:** **Commander Cast Avg accelerated to T3.5**, **Cast Rate increased to 95%**, **Engine Readiness hit T4.3**, and **Gold Keeps reached 62.5%**.

---

## [2026-08-20] — Ramp-Optimized Upgrade (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_204755.html
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
  Commander cast rate: 74/80 (92%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.8
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   48/80 (60%)
    Silver Keep (Mana + Curve):          32/80 (40%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.97 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 70/80 (88%)
  Engine Readiness Avg:  T4.5
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.5, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
