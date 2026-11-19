# Goldfish Simulation Log: Valgavoth, Harrower of Souls (Endless Punishment)

## 2026-11-18 — Precon Baseline Audit (20 sims, T10 turns, Bracket 2)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Owned/ValgavothEndlessPunishment/moxfield_import.txt" --sims 20 --turns 10 --bracket 2
```

**Results:**
```text
--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.9
  Commander Cast Distribution:
    T 2: ###### (6)
    T 3: ######################## (24)
    T 4: ################################# (33)
    T 5: ############ (12)
    T 6: ### (3)
    T 8: # (1)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   28/80 (35%)
    Silver Keep (Mana + Curve):          52/80 (65%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.97 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 2 (Core) — Target T9)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=9): 78/80 (98%)
  Engine Readiness Avg:  T4.6
  Engine Readiness Distribution:
    T 3: ############# (13)
    T 4: ############################### (31)
    T 5: ######################### (25)
    T 6: ###### (6)
    T 7: ### (3)
    T10: ## (2)
```

**Notes:**
* **Flawless Deployment:** 100% cast rate across 80 seats with an average deployment turn of **T3.9** (79% cast on or before Turn 4).
* **High Keep Stability:** 0% desperation keeps and an average starting hand size of 6.97 cards.
* **Engine Velocity:** Precon achieves engine readiness by **Turn 4.6** on average. The simulator flags this as hyper-fast for Bracket 2, confirming that Valgavoth is already primed to transition into a robust Bracket 3 engine once the taplands and filter pieces are cleaned up.
