# Goldfish Log — Rocco, Street Chef ("The Street Chef's Kitchen")

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
