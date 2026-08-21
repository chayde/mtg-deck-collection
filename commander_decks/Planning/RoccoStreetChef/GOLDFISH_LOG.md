# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

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
  Commander Cast Distribution:
    T 1: ### (3)
    T 2: ########################### (27)
    T 3: ############################ (28)
    T 4: ############# (13)
    T 5: ### (3)
    T 6: ### (3)
    T 7: # (1)
    T 8: ## (2)

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
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ######################## (24)
    T 4: ############################ (28)
    T 5: ############### (15)
    T 6: ##### (5)
    T 7: ## (2)
    T 8: ### (3)
    T 9: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.2, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Swaps Executed:** Replaced *Flawless Maneuver* ($20.22) with **Baylen, the Haymaker** ($0.23), *Boseiju* ($51.38) with Basic Forest, and *Mana Confluence* ($34.93) with *Path of Ancestry*.
- **Impact:** Total deck cost dropped to **$264.69** (-63.4% overall savings!). **Commander cast avg accelerated to T3.1**, **Cast rate hit 100%**, and **Target window readiness reached 95%**.

---

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
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
