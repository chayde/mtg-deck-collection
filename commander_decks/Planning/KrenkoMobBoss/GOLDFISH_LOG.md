# Goldfish Simulation Log: Krenko, Mob Boss

## 2026-09-21 — Option 1 Post-Ban Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/KrenkoMobBoss/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html "commander_decks/Planning/KrenkoMobBoss/goldfish_report.html"
```

**Results:**
```
--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T2 - T7
  Commander Cast Avg:   T3.8
  Commander Cast Distribution:
    T 2: ###### (6)
    T 3: ############################ (28)
    T 4: ############################# (29)
    T 5: ############ (12)
    T 6: ### (3)
    T 7: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   42/80 (52%)
    Silver Keep (Mana + Curve):          37/80 (46%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.92 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 77/80 (96%)
  Engine Readiness Avg:  T4.3
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: #################### (20)
    T 4: ############################## (30)
    T 5: ################ (16)
    T 6: ##### (5)
    T 7: #### (4)
    T 8: ## (2)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.3, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
* **Fast Acceleration:** Krenko drops by Turn 3 or 4 in 79% of simulated games (T3.8 average), with explosive Turn 2 deployments when hitting *Ancient Tomb*, *Mox Diamond*, or *Sol Ring*.
* **Mulligan Stability:** 98% of hands were Gold or Silver keeps (6.92 avg hand size), with only 1 desperation keep across 80 evaluated seats.
* **Engine Velocity:** 96% of games achieved full engine readiness by or before the Bracket 3 target window (T7), averaging T4.3.
* **Post-Ban Health:** Replacing Jeweled Lotus, Mana Crypt, and Mox Ruby with Arcane Signet, Patriar's Seal, and Umbral Mantle successfully preserved competitive velocity while bringing the list into full legal compliance for Bracket 3 (3/3 Game Changers).
