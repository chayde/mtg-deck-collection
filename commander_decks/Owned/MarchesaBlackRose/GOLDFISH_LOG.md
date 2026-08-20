# Goldfish Simulation Log: Marchesa, the Black Rose (The Iron Throne)

## [2026-08-20] — Bracket Audit Test (Bracket 3 Validated) (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Owned/MarchesaBlackRose/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Owned/MarchesaBlackRose/goldfish_audit_20260820_181239.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Marchesa, the Black Rose (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 77/80 (96%)
  Commander Cast Range: T1 - T7
  Commander Cast Avg:   T3.2
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   40/80 (50%)
    Silver Keep (Mana + Curve):          39/80 (49%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.89 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 74/80 (92%)
  Engine Readiness Avg:  T3.9
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 3.9, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- **Validated Bracket 3 Position:** 0 Game Changers. Marchesa deploys on T3.2 on average with 10 mana rocks, assembling 3-to-4 card Aristocrat loop engines by T3.9.

---

## 🏆 Goldfish Game 1 (Ideal Aggressive Engine)
**Starting Hand:** Shivan Reef, Sage of Fables, Iron Apprentice, An Offer You Can't Refuse, Swamp, Juri, Watery Grave.
**Draws:** Goblin Bombardment, Swamp, Mountain, Dragonskull Summit, Sunken Hollow, Rakdos Signet, Bedevil, Reanimate, Toxic Deluge, Phyrexian Altar.

*   **Turn 1:** Iron Apprentice (Enters with counter).
*   **Turn 2:** Juri, Master of the Revue.
*   **Turn 3:** Goblin Bombardment (Engine Online).
*   **Turn 4:** Marchesa. Loop Iron Apprentice on every turn. Juri scales to 9/9 by T5.
*   **Turn 5:** Sage of Fables (Draw engine + Insurance).
*   **Turn 6+:** Infinite scaling. Toxic Deluge is one-sided. Game essentially over via Juri explosion or repeated pings.

---

## 🐢 Goldfish Game 2 (Reactive Midrange Recovery)
**Starting Hand:** Zealous Conscripts, Chasm Skulker, Chaos Warp, Feed the Swarm, Mountain, Drowned Catacomb, Island.
**Draws:** Immersturm Predator, Crumbling Necropolis, Midnight Reaper, The Ozolith, Evolving Wilds, Path of Ancestry, Sage of Fables, Talisman of Dominance, Satoru the Infiltrator, Reanimate.

*   **Turn 1-2:** Land setup (Island into T2 Crumbling Necropolis).
*   **Turn 3:** Chasm Skulker. Starts growing from draws.
*   **Turn 4:** The Ozolith. (Critical insurance).
*   **Turn 5:** Immersturm Predator. (Free sacrifice outlet).
*   **Turn 6:** Marchesa (Land: Path of Ancestry).
*   **Turn 7:** Sage of Fables.
*   **Synergy Check:** We now have a "Safe" sacrifice loop. Chasm Skulker dies -> tokens created -> counters move to The Ozolith -> Ozolith moves counters back to Skulker on combat -> Marchesa returns Skulker at end step.
*   **Turn 8-10:** Satoru and Midnight Reaper provide massive card draw whenever things enter or die. Reanimate keeps Marchesa on board if she is ever removed before a counter lands.

---
## 📊 Summary of Findings
1.  **Resilience:** Even in Game 2, where we missed early ramp, the "Enter with Counter" (Chasm Skulker/Predator) and "Counter Insurance" (The Ozolith) made the board state incredibly sticky by Turn 5.
2.  **Interaction:** The deck naturally draws into interaction (Chaos Warp, Bedevil, Offer You Can't Refuse) while building its board.
3.  **Independence:** Neither game required us to be at low life to function. Dethrone was a "bonus" rather than a requirement.
