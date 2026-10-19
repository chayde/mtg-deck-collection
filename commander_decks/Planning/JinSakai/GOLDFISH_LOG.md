# Goldfish Simulation Log: Jin Sakai, Ghost of Tsushima

## [2026-10-18] — Initial Low Bracket 3 Baseline Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/JinSakai/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```text
--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T3 - T10
  Commander Cast Avg:   T5.0
  Commander Cast Distribution:
    T 3: ####### (7)
    T 4: ########################## (26)
    T 5: ################################# (33)
    T 6: ### (3)
    T 7: ### (3)
    T 8: #### (4)
    T 9: ### (3)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   44/80 (55%)
    Silver Keep (Mana + Curve):          36/80 (45%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.99 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 72/80 (90%)
  Engine Readiness Avg:  T5.2
  Engine Readiness Distribution:
    T 3: ### (3)
    T 4: ##################### (21)
    T 5: ######################################## (40)
    T 6: ##### (5)
    T 7: ### (3)
    T 8: ### (3)
    T 9: #### (4)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 5.2, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
* Replacing the LGS list's 5-rock Signet package with an 11-card non-Signet ramp suite (*Talismans*, *Arcane Signet*, *Fellwar Stone*, *Sol Ring*, *Wayfarer's Bauble*, *Ornithopter of Paradise*, *Loyal Warhound*, *Lotho*, *Sword of the Animist*) more than doubled the **Gold Keep rate from 21% to 55%** with **0% Desperation Keeps (6.99 avg hand size)** and **100% Commander Cast Rate (80/80)** while using a budget-friendly Esper land base.
* **Engine Readiness averages Turn 5.2 (90% $\le$ T7)**, placing the deck cleanly in **Low Bracket 3 (DTI 33/96)** with zero Game Changers.
