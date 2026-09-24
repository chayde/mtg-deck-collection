# Goldfish Simulation Log: KrenkoBracket3

## 2026-09-24 — Baseline Architecture Benchmark (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/KrenkoBracket3/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html "commander_decks/Planning/KrenkoBracket3/goldfish_report.html"
```

**Results:**
```
--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T2 - T8
  Commander Cast Avg:   T3.9
  Commander Cast Distribution:
    T 2: ###### (6)
    T 3: ###################### (22)
    T 4: #################################### (36)
    T 5: ########## (10)
    T 6: #### (4)
    T 7: # (1)
    T 8: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   40/80 (50%)
    Silver Keep (Mana + Curve):          39/80 (49%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.95 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 76/80 (95%)
  Engine Readiness Avg:  T4.6
  Engine Readiness Distribution:
    T 2: ### (3)
    T 3: ############# (13)
    T 4: ########################### (27)
    T 5: ##################### (21)
    T 6: ####### (7)
    T 7: ##### (5)
    T 8: ### (3)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.6, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
*   **100% Commander Cast Rate:** Krenko hit the board in all 80 seat games, averaging **Turn 3.9**, with 28 games (35%) casting Krenko on Turn 2 or 3 via *Sol Ring*, *Skirk Prospector*, *Brightstone Ritual*, or *Fellwar Stone*.
*   **Exceptional Mulligan Stability:** 99% functional opening hands (50% Gold, 49% Silver, only 1 desperation keep) with an average starting hand size of 6.95 cards. The mono-red mana base and low curve virtually eliminate color-screw.
*   **Decisive Bracket 3 Compliance:** 95% target window readiness ($\le$ T7), averaging Turn 4.6 engine readiness, securing an unambiguous **PASS** for Bracket 3.
*   **The 9-Source Haste Matrix & Protection:** Haste enablers (*Lightning Greaves*, *Swiftfoot Boots*, *The Fire Crystal*, *Rising of the Day*, *Thousand-Year Elixir*) consistently eliminated summoning sickness downtime, while *Deflecting Swat* and *Return the Favor* stood ready to shield Krenko on deployment.
