# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

## [2026-08-31] — Samwise Gamgee & Syr Ginger Theme Integration (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3
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
  Commander Cast Avg:   T2.9
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ################################# (33)
    T 3: ############################### (31)
    T 4: ######### (9)
    T 5: #### (4)
    T 6: # (1)
    T 8: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   54/80 (68%)
    Silver Keep (Mana + Curve):          26/80 (32%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.97 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 79/80 (99%)
  Engine Readiness Avg:  T3.8
  Engine Readiness Distribution:
    T 2: ####### (7)
    T 3: ########################## (26)
    T 4: ############################## (30)
    T 5: ########### (11)
    T 6: ### (3)
    T 7: ## (2)
    T 8: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 3.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **On-Theme Swaps:** Replaced *Etali, Primal Storm* (6 CMC) and *Gwaihir, Greatest of the Eagles* (5 CMC) with **Samwise Gamgee** ({G}{W} — *Food creation + historic recursion*) and **Syr Ginger, the Meal Ender** ({2} — *Artifact sacrifice +1/+1 counters + scry filtering + life gain*).
- **Velocity Improvement:** Lowering the curve improved early-game hand cohesion and accelerated Engine Readiness to **T3.8 average** with **68% Gold Keeps**, **100% functional keeps (0% desperation keeps)**, and **100% commander cast rate (80/80, T2.9 avg)**.

---

## [2026-08-20] — Killer Service Integration Audit (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_221838.html
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
  Commander Cast Range: T2 - T6
  Commander Cast Avg:   T2.8
  Commander Cast Distribution:
    T 2: ############################### (31)
    T 3: #################################### (36)
    T 4: ######### (9)
    T 5: ### (3)
    T 6: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   52/80 (65%)
    Silver Keep (Mana + Curve):          28/80 (35%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          7.00 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 80/80 (100%)
  Engine Readiness Avg:  T4.0
  Engine Readiness Distribution:
    T 2: #### (4)
    T 3: ######################## (24)
    T 4: ############################## (30)
    T 5: ################# (17)
    T 6: #### (4)
    T 7: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.0, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Killer Service Integration:** Replaced *Sovereign Okinec Ahau* ($2.95) with **Killer Service** ({2}{G} — *ETB 3 Food tokens + sac a Food at end step to create a 4/4 Rhino Warrior*). Added *Mondrak* ($41) and *Krark-Clan Ironworks* ($17) to `Future Roadmap / Upgrades`.
- **Impact:** **Target Window Readiness hit 100% (80/80)**, **Commander cast avg accelerated to T2.8**, **Cast rate hit 100%**, **Gold Keeps hit 65%**, and **Desperation Keeps dropped to 0%**.

---

## [2026-08-20] — Verified 100-Card Deck Audit ($239 Budget) (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Planning/RoccoStreetChef/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Planning/RoccoStreetChef/goldfish_audit_20260820_212240.html
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
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T2.9
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   46/80 (57%)
    Silver Keep (Mana + Curve):          33/80 (41%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.95 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 77/80 (96%)
  Engine Readiness Avg:  T3.9
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 3.9, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```
