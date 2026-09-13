# Goldfish Simulation Log: Ultron, Artificial Malevolence

This document tracks all goldfish simulations, opening hand analyses, commander deployment pacing, and bracket engine readiness benchmarks for **Ultron, Artificial Malevolence** ({3}) using `scripts/multiplayer_goldfish.py`.

---

## 2026-09-13 — Baseline 20-Game Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/UltronArtificialMalevolence/moxfield_import.txt" --sims 20 --turns 10 --bracket 3 --html "commander_decks/Planning/UltronArtificialMalevolence/goldfish_report.html"
```

**Results:**
```text
--------------------------------------------------------------------
FASTEST COMMANDER DEPLOYMENT SHOWCASE (Sim 11, Seat 4)
--------------------------------------------------------------------
  Cast Turn:     Turn 1 (Gold Keep, 6 cards)
  Opening Hand:  Sol Ring, Ugin, Eye of the Storms, Liberator, Urza's Battlethopter, Radiant Lotus, Shrine of the Forsaken Gods, Wastes
  Deployment Sequence:
    T 1: Land: Shrine of the Forsaken Gods | Cast: Sol Ring | ** CAST Ultron, Artificial Malevolence T1 **

--------------------------------------------------------------------
WORST-CASE COMMANDER DEPLOYMENT SHOWCASE (Sim 1, Seat 2)
--------------------------------------------------------------------
  Status:        Turn 9 (Late Deployment)
  Mulligan:      Gold Keep (7 cards)
  Diagnostic:    Late Deployment: Cast on Turn 9 due to slow early mana acceleration or tapped lands
  Opening Hand:  Radiant Lotus, Voltaic Key, Talon Gates of Madara, Iron Spider, Stark Upgrade, Wastes, Ugin, the Spirit Dragon, Hedron Archive
  Turn-by-Turn Play Sequence:
    T 1: Land: Talon Gates of Madara | Cast: Voltaic Key (generic)
    T 2: Land: Wastes
    T 3: (no plays)
    T 4: (no plays)
    T 5: (no plays)
    T 6: (no plays)
    T 7: (no plays)
    T 8: Land: Thespian's Stage | Cast: Agility Bobblehead
    T 9: Land: Darksteel Citadel | Cast: Hedron Archive | ** CAST Ultron, Artificial Malevolence T9 **
    T10: Land: Haven of the Spirit Dragon | Cast: Radiant Lotus (generic)

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 80/80 (100%)
  Commander Cast Range: T1 - T9
  Commander Cast Avg:   T3.7
  Commander Cast Distribution:
    T 1: # (1)
    T 2: ###### (6)
    T 3: ################################## (34)
    T 4: ###################### (22)
    T 5: ############ (12)
    T 6: ### (3)
    T 7: # (1)
    T 9: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   43/80 (54%)
    Silver Keep (Mana + Curve):          37/80 (46%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.97 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 78/80 (98%)
  Engine Readiness Avg:  T4.5
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ######### (9)
    T 4: ###################################### (38)
    T 5: ###################### (22)
    T 6: #### (4)
    T 7: #### (4)
    T 8: # (1)
    T 9: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.5, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
*   **Rapid Commander Deployment:** Ultron's low 3-CMC colorless cost allows consistent early deployment (**100% cast rate**, **T3.7 average**). 51% of games saw Ultron cast on or before Turn 3.
*   **Pristine Hand Stability:** 100% functional keeps (54% Gold Keeps, 46% Silver Keeps) with **zero desperation keeps** and an average starting hand size of 6.97.
*   **Engine Velocity:** 98% of games achieved engine readiness within the Bracket 3 target window (by Turn 7), with an average engine activation turn of **Turn 4.5**.
*   **Stall Outlier Observation:** The single Turn 9 late deployment in Sim 1 Seat 2 occurred due to opening a hand with high-CMC cards and drawing several lands that couldn't cast early 3-CMC rocks until Turn 8. Adding lower-CMC card selection (e.g. *Mystic Forge*, *Sensei's Divining Top*) will further eliminate topdeck land stalls.
