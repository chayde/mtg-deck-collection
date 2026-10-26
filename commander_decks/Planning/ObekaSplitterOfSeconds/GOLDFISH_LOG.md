# Goldfish Simulation Log: Obeka, Splitter of Seconds

## [2026-10-26] — Initial 100-Card Candidate Baseline Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/ObekaSplitterOfSeconds/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```text
--------------------------------------------------------------------
FASTEST COMMANDER DEPLOYMENT SHOWCASE (Sim 2, Seat 3)
--------------------------------------------------------------------
  Cast Turn:     Turn 3 (Silver Keep, 7 cards)
  Opening Hand:  Brotherhood Regalia, Mountain, Island, Skyline Despot, Rilsa Rael, Kingpin, Court of Ire, Polluted Delta
  Deployment Sequence:
    T 1: Land: Polluted Delta | Cast: Sol Ring | Cast: Brotherhood Regalia (generic)
    T 2: Land: Mountain
    T 3: Land: Island | ** CAST Obeka, Splitter of Seconds T3 **

--------------------------------------------------------------------
WORST-CASE COMMANDER DEPLOYMENT SHOWCASE (Sim 10, Seat 4)
--------------------------------------------------------------------
  Status:        FAILED TO CAST (through Turn 10)
  Mulligan:      Silver Keep (7 cards)
  Diagnostic:    Curve / Timing Stall: Reached 9 mana across 5 lands, but could not satisfy pip combination ({U} {B} {R}) simultaneously
  Opening Hand:  Mountain, Trailblazer's Boots, Phyrexian Arena, Terminate, Winged Boots, Mountain, Island
  Turn-by-Turn Play Sequence:
    T 1: Land: Mountain
    T 2: Land: Mountain | Cast: Izzet Signet
    T 3: Land: Island | Cast: Trailblazer's Boots (generic) | Cast: Winged Boots (generic)
    T 4: Land: Steam Vents (tapped) | Cast: Paradox Haze (generic)
    T 5: Cast: Court of Vantress (generic)
    T 6: Cast: Lightning Greaves (generic)
    T 7: Cast: Sol Ring
    T 8: Cast: Talisman of Indulgence
    T 9: Cast: Court of Ire (generic)
    T10: Land: Watery Grave (tapped)

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T3 - T10
  Commander Cast Avg:   T4.7
  Commander Cast Distribution:
    T 3: ############# (13)
    T 4: ################################### (35)
    T 5: ################ (16)
    T 6: ###### (6)
    T 7: ### (3)
    T 8: ### (3)
    T 9: ## (2)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   35/80 (44%)
    Silver Keep (Mana + Curve):          43/80 (54%)
    Desperation Keep (Mulligan to <=5):   2/80 (2%)
    Average Starting Hand Size:          6.90 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 69/80 (86%)
  Engine Readiness Avg:  T5.1
  Engine Readiness Distribution:
    T 3: #### (4)
    T 4: ################################# (33)
    T 5: #################### (20)
    T 6: ######### (9)
    T 7: ### (3)
    T 8: ##### (5)
    T 9: #### (4)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 5.1, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
* **Strong Core Tempo (T4.7 Avg Cast, T5.1 Avg Engine Readiness):** In 48 of 80 seats (60%), **Obeka, Splitter of Seconds** deploys on Turn 3 or Turn 4, and 86% of seats reach full Bracket 3 Engine Readiness by Turn $\le 7$.
* **Empirical Proof of the 35-Land Deficit & Filter Signet Friction:**
  * Even with 10 mana rocks/reducers, running **35 lands** in a 3-color Grixis deck caused **15 seats (18.8%)** to be delayed until Turn 6–10 (and 1 seat in Sim 10 Seat 4 to stall completely on 4 lands from Turn 4 to Turn 9 without `{B}` access).
  * Furthermore,Gold Keeps sit at **44%** (with 2 Desperation Keeps). Upgrading the 3 filter Signets (*Rakdos Signet*, *Izzet Signet*, *Dimir Signet*) to rainbow/synergy ramp (*Fellwar Stone*, *Midnight Clock*, *Sword of the Animist*) and increasing the land count from **35 $\rightarrow$ 38** (*Underground River*, *Haunted Ridge*, +1 basic land) is projected to push Gold Keeps past 55% and eliminate late-turn land stalls.
