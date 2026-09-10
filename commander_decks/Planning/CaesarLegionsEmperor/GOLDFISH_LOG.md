# Goldfish Simulation Log: Caesar, Legion's Emperor

Simulation logs and performance validation across iterations for **Caesar, Legion's Emperor** ({1}{R}{W}{B}).

---

## 2026-09-10 — Initial Inception & Baseline Trial (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/CaesarLegionsEmperor/moxfield_import.txt" --bracket 3 --sims 20 --turns 10
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Caesar, Legion's Emperor (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

  Sim 1: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 2, 2, 4]  |  Avg creatures: 2.8
  Sim 2: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 6, 6, 2]  |  Avg creatures: 4.0
  Sim 3: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 3, 5]  |  Avg creatures: 4.5
  Sim 4: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 5, 4]  |  Avg creatures: 2.8
  Sim 5: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 3, 6]  |  Avg creatures: 3.2
  Sim 6: Commander cast 4/4  |  Earliest: T3    |  Turns: [3, 4, 4, 3]  |  Avg creatures: 2.5
  Sim 7: Commander cast 4/4  |  Earliest: T1    |  Turns: [3, 4, 3, 1]  |  Avg creatures: 4.5
  Sim 8: Commander cast 4/4  |  Earliest: T2    |  Turns: [6, 2, 4, 2]  |  Avg creatures: 3.8
  Sim 9: Commander cast 4/4  |  Earliest: T4    |  Turns: [4, 7, 5, 7]  |  Avg creatures: 3.8
  Sim 10: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 2, 2, 2]  |  Avg creatures: 4.5
  Sim 11: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 4, 4, 3]  |  Avg creatures: 3.2
  Sim 12: Commander cast 4/4  |  Earliest: T2    |  Turns: [4, 5, 2, 3]  |  Avg creatures: 3.2
  Sim 13: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 3, 4, 2]  |  Avg creatures: 2.5
  Sim 14: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 4, 2, 3]  |  Avg creatures: 3.0
  Sim 15: Commander cast 4/4  |  Earliest: T2    |  Turns: [3, 5, 2, 3]  |  Avg creatures: 4.0
  Sim 16: Commander cast 4/4  |  Earliest: T2    |  Turns: [8, 4, 3, 2]  |  Avg creatures: 3.5
  Sim 17: Commander cast 4/4  |  Earliest: T2    |  Turns: [8, 2, 3, 5]  |  Avg creatures: 4.5
  Sim 18: Commander cast 4/4  |  Earliest: T2    |  Turns: [2, 3, 2, 4]  |  Avg creatures: 2.2
  Sim 19: Commander cast 3/4  |  Earliest: T2    |  Turns: [2, 3, 3]  |  Avg creatures: 4.0
  Sim 20: Commander cast 4/4  |  Earliest: T1    |  Turns: [5, 3, 3, 1]  |  Avg creatures: 3.2

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T1 - T8
  Commander Cast Avg:   T3.5
  Commander Cast Distribution:
    T 1: ## (2)
    T 2: #################### (20)
    T 3: ######################### (25)
    T 4: ################# (17)
    T 5: ####### (7)
    T 6: #### (4)
    T 7: ## (2)
    T 8: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   38/80 (48%)
    Silver Keep (Mana + Curve):          39/80 (49%)
    Desperation Keep (Mulligan to <=5):   3/80 (4%)
    Average Starting Hand Size:          6.86 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 73/80 (91%)
  Engine Readiness Avg:  T4.4
  Engine Readiness Distribution:
    T 1: # (1)
    T 2: ####### (7)
    T 3: ################### (19)
    T 4: ################## (18)
    T 5: #################### (20)
    T 6: ##### (5)
    T 7: ### (3)
    T 8: #### (4)
    T 9: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
*   **Rapid Commander Deployment:** 99% overall cast rate with an average deployment turn of **T3.5**. In 59% of games (47/80), Caesar was on the battlefield on or before Turn 3.
*   **Rock-Solid Opening Quality:** 97% functional hands (48% Gold Keeps, 49% Silver Keeps), with only a 4% desperation mulligan rate and an average hand size of 6.86.
*   **Target Bracket Alignment:** Achieves Engine Readiness on average at **T4.4**, with 91% readiness within the target window (<= Turn 7), cleanly passing the Bracket 3 compliance check.

---

## 2026-09-10 — Post-Engine Mana Audit & Sequence Tracking Validation (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/CaesarLegionsEmperor/moxfield_import.txt" --bracket 3 --sims 20 --turns 10 --html commander_decks/Planning/CaesarLegionsEmperor/goldfish_report.html
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Caesar, Legion's Emperor (CMC 4)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

  Sim  1: Commander cast 4/4  |  Earliest: T3   (Seat 3, Gold Keep)  |  Turns: [5, 6, 3, 4]  |  Avg creatures: 4.8
         Hand: [Boros Charm, Call the Coppercoats, Talisman of Hierarchy, Battlefield Forge, Windbrisk Heights, Sacred Foundry, Sulfurous Springs]
         Line: T 1: Land: Battlefield Forge -> T 2: Land: Sulfurous Springs | Cast: Talisman of Hierarchy -> T 3: Land: Prismatic Vista | ** CAST Caesar, Legion's Emperor T3 **
  Sim  2: Commander cast 4/4  |  Earliest: T4   (Seat 2, Gold Keep)  |  Turns: [6, 4, 4, 4]  |  Avg creatures: 4.5
         Hand: [Shadowblood Ridge, Diamond City, Purphoros, God of the Forge, Orzhov Signet, Loyal Apprentice, Fellwar Stone, Isshin, Two Heavens as One]
         Line: T 1: Land: Shadowblood Ridge -> T 2: Land: Sulfurous Springs | Cast: Orzhov Signet -> T 3: Land: Diamond City | Cast: Fellwar Stone | Cast: Deadly Dispute | Cast: Loyal Apprentice (generic) -> T 4: ** CAST Caesar, Legion's Emperor T4 **
  Sim  3: Commander cast 4/4  |  Earliest: T3   (Seat 2, Gold Keep)  |  Turns: [4, 3, 5, 5]  |  Avg creatures: 2.8
         Hand: [Bloodstained Mire, Call the Coppercoats, Fellwar Stone, Plains, Generous Gift, Shadowblood Ridge, Anguished Unmaking]
         Line: T 1: Land: Shadowblood Ridge -> T 2: Land: Bloodstained Mire | Cast: Fellwar Stone -> T 3: Land: Plains | ** CAST Caesar, Legion's Emperor T3 **
  Sim  4: Commander cast 4/4  |  Earliest: T2   (Seat 2, Gold Keep)  |  Turns: [5, 2, 4, 3]  |  Avg creatures: 2.8
         Hand: [Caves of Koilos, Arcane Signet, Myrel, Shield of Argive, Martial Coup, Castle Ardenvale, Talisman of Conviction, Plains]
         Line: T 1: Land: Caves of Koilos | Cast: Sol Ring | Cast: Arcane Signet -> T 2: Land: Plains | Cast: Talisman of Conviction | ** CAST Caesar, Legion's Emperor T2 **
  Sim  5: Commander cast 4/4  |  Earliest: T4   (Seat 2, Silver Keep)  |  Turns: [7, 4, 4, 4]  |  Avg creatures: 2.8
         Hand: [Savai Triome, Flawless Maneuver, Sol Ring, Plains, Castle Ardenvale, Mountain]
         Line: T 1: Land: Plains | Cast: Sol Ring -> T 2: Land: Mountain | Cast: Flawless Maneuver (generic) -> T 3: Land: Savai Triome (tapped) | Cast: Anointed Procession (generic) -> T 4: Land: Prismatic Vista | ** CAST Caesar, Legion's Emperor T4 **
  Sim  6: Commander cast 4/4  |  Earliest: T3   (Seat 3, Gold Keep)  |  Turns: [6, 6, 3, 7]  |  Avg creatures: 3.2
         Hand: [Idol of Oblivion, Marsh Flats, Grand Crescendo, Desolate Mire, Adeline, Resplendent Cathar, Talisman of Conviction, Mountain]
         Line: T 1: Land: Desolate Mire -> T 2: Land: Marsh Flats | Cast: Talisman of Conviction -> T 3: Land: Mountain | ** CAST Caesar, Legion's Emperor T3 **
  Sim  7: Commander cast 4/4  |  Earliest: T3   (Seat 2, Gold Keep)  |  Turns: [6, 3, 4, 4]  |  Avg creatures: 3.2
         Hand: [Zulaport Cutthroat, Boros Signet, Command Tower, Warleader's Call, Caves of Koilos, Blood Crypt, Sol Ring]
         Line: T 1: Land: Command Tower | Cast: Sol Ring | Cast: Boros Signet -> T 2: Land: Caves of Koilos | Cast: Pitiless Plunderer -> T 3: Land: Shadowblood Ridge | ** CAST Caesar, Legion's Emperor T3 **
  Sim  8: Commander cast 4/4  |  Earliest: T3   (Seat 4, Gold Keep)  |  Turns: [4, 6, 5, 3]  |  Avg creatures: 2.5
         Hand: [Phyrexian Tower, Anointed Procession, Wear // Tear, Teysa Karlov, Godless Shrine, Deadly Dispute, Plains]
         Line: T 1: Land: Phyrexian Tower -> T 2: Land: Plains | Cast: Deadly Dispute -> T 3: Land: Plains | ** CAST Caesar, Legion's Emperor T3 **
  Sim  9: Commander cast 4/4  |  Earliest: T4   (Seat 1, Gold Keep)  |  Turns: [4, 4, 4, 4]  |  Avg creatures: 2.2
         Hand: [Isolated Chapel, Stroke of Midnight, Sacred Foundry, Skullclamp, Teferi's Protection, Sol Ring, Horn of Gondor]
         Line: T 1: Land: Isolated Chapel (tapped) -> T 2: Land: Sacred Foundry (tapped) | Cast: Sol Ring | Cast: Skullclamp (generic) -> T 3: Land: Castle Ardenvale (tapped) | Cast: Stroke of Midnight (generic) -> T 4: Land: Desolate Mire | ** CAST Caesar, Legion's Emperor T4 **
  Sim 10: Commander cast 4/4  |  Earliest: T4   (Seat 1, Gold Keep)  |  Turns: [4, 5, 4, 6]  |  Avg creatures: 3.2
         Hand: [Boros Signet, Talisman of Indulgence, Ruinous Ultimatum, Martial Coup, Swamp, Flawless Maneuver, Exotic Orchard]
         Line: T 1: Land: Swamp -> T 2: Land: Exotic Orchard | Cast: Boros Signet -> T 3: Land: Plains | Cast: Talisman of Indulgence | Cast: Martial Coup (generic) -> T 4: ** CAST Caesar, Legion's Emperor T4 **
  Sim 11: Commander cast 4/4  |  Earliest: T4   (Seat 3, Gold Keep)  |  Turns: [5, 5, 4, 4]  |  Avg creatures: 3.0
         Hand: [Anguished Unmaking, Path of Ancestry, Skullclamp, Swamp, General's Enforcer, Command Tower, Talisman of Hierarchy]
         Line: T 1: Land: Command Tower | Cast: Skullclamp (generic) -> T 2: Land: Swamp | Cast: Talisman of Hierarchy -> T 3: Land: Path of Ancestry (tapped) | Cast: Anguished Unmaking (generic) -> T 4: ** CAST Caesar, Legion's Emperor T4 **
  Sim 12: Commander cast 4/4  |  Earliest: T4   (Seat 3, Gold Keep)  |  Turns: [6, 5, 4, 5]  |  Avg creatures: 3.8
         Hand: [Caves of Koilos, Welcoming Vampire, Mountain, Battlefield Forge, Talisman of Hierarchy, Charismatic Conqueror, Bastion of Remembrance]
         Line: T 1: Land: Caves of Koilos -> T 2: Land: Battlefield Forge | Cast: Talisman of Hierarchy -> T 3: Land: Mountain | Cast: Orzhov Signet | Cast: Welcoming Vampire (generic) -> T 4: Land: Dragonskull Summit (tapped) | ** CAST Caesar, Legion's Emperor T4 **
  Sim 13: Commander cast 4/4  |  Earliest: T3   (Seat 4, Gold Keep)  |  Turns: [8, 4, 4, 3]  |  Avg creatures: 3.0
         Hand: [Swamp, Smoldering Marsh, Ruinous Ultimatum, Zulaport Cutthroat, Mirkwood Bats, Clifftop Retreat, Sol Ring]
         Line: T 1: Land: Swamp | Cast: Sol Ring -> T 2: Land: Smoldering Marsh (tapped) | Cast: Fellwar Stone | Cast: Zulaport Cutthroat (generic) -> T 3: Land: Clifftop Retreat (tapped) | ** CAST Caesar, Legion's Emperor T3 **
  Sim 14: Commander cast 4/4  |  Earliest: T3   (Seat 2, Gold Keep)  |  Turns: [5, 3, 4, 6]  |  Avg creatures: 2.8
         Hand: [Flawless Maneuver, Talisman of Indulgence, Chaos Warp, Sulfurous Springs, Wear // Tear, Prismatic Vista, Caves of Koilos]
         Line: T 1: Land: Sulfurous Springs -> T 2: Land: Prismatic Vista | Cast: Talisman of Indulgence -> T 3: Land: Caves of Koilos | ** CAST Caesar, Legion's Emperor T3 **
  Sim 15: Commander cast 4/4  |  Earliest: T3   (Seat 1, Gold Keep)  |  Turns: [3, 6, 4, 5]  |  Avg creatures: 3.0
         Hand: [Swords to Plowshares, Charismatic Conqueror, Sulfurous Springs, Plains, Sol Ring, Welcoming Vampire, Shadowblood Ridge]
         Line: T 1: Land: Sulfurous Springs | Cast: Sol Ring -> T 2: Land: Shadowblood Ridge -> T 3: Land: Plains | ** CAST Caesar, Legion's Emperor T3 **
  Sim 16: Commander cast 4/4  |  Earliest: T4   (Seat 1, Silver Keep)  |  Turns: [4, 4, 4, 5]  |  Avg creatures: 3.5
         Hand: [Shadowblood Ridge, Swamp, Anim Pakal, Thousandth Moon, Sulfurous Springs, Marsh Flats, Desolate Mire, Skullclamp]
         Line: T 1: Land: Shadowblood Ridge -> T 2: Land: Sulfurous Springs | Cast: Skullclamp (generic) -> T 3: Land: Desolate Mire | Cast: Anim Pakal, Thousandth Moon (generic) -> T 4: Land: Swamp | ** CAST Caesar, Legion's Emperor T4 **
  Sim 17: Commander cast 4/4  |  Earliest: T4   (Seat 2, Gold Keep)  |  Turns: [5, 4, 9, 5]  |  Avg creatures: 2.8
         Hand: [Chaos Warp, Boros Signet, Flawless Maneuver, Swamp, Generous Gift, Diamond City, Mountain]
         Line: T 1: Land: Swamp -> T 2: Land: Diamond City | Cast: Boros Signet -> T 3: Land: Mountain | Cast: Orzhov Signet | Cast: Flawless Maneuver (generic) -> T 4: ** CAST Caesar, Legion's Emperor T4 **
  Sim 18: Commander cast 4/4  |  Earliest: T5   (Seat 1, Silver Keep)  |  Turns: [5, 5, 5, 7]  |  Avg creatures: 2.2
         Hand: [Pitiless Plunderer, Plains, Castle Ardenvale, Plains, Wear // Tear, Diamond City, Swamp]
         Line: T 1: Land: Plains -> T 2: Land: Plains | Cast: Swords to Plowshares (generic) -> T 3: Land: Diamond City | Cast: Stroke of Midnight (generic) -> T 4: Land: Swamp | Cast: Pitiless Plunderer -> T 5: Land: Shadowblood Ridge | ** CAST Caesar, Legion's Emperor T5 ** | Cast: Wear // Tear (generic)
  Sim 19: Commander cast 3/4  |  Earliest: T4   (Seat 2, Silver Keep)  |  Turns: [4, 5, 10]  |  Avg creatures: 2.2
         Hand: [Mountain, Sulfurous Springs, Swamp, Command Tower, Ruinous Ultimatum, Diamond City, Liliana, Dreadhorde General]
         Line: T 1: Land: Sulfurous Springs -> T 2: Land: Command Tower | Cast: Impact Tremors (generic) -> T 3: Land: Mountain | Cast: Skullclamp (generic) -> T 4: Land: Swamp | ** CAST Caesar, Legion's Emperor T4 **
  Sim 20: Commander cast 4/4  |  Earliest: T3   (Seat 1, Gold Keep)  |  Turns: [3, 4, 4, 4]  |  Avg creatures: 2.8
         Hand: [Sulfurous Springs, Secure the Wastes, Teferi's Protection, Talisman of Conviction, Call the Coppercoats, Plains, Prismatic Vista]
         Line: T 1: Land: Sulfurous Springs -> T 2: Land: Prismatic Vista | Cast: Talisman of Conviction -> T 3: Land: Plains | ** CAST Caesar, Legion's Emperor T3 **

--------------------------------------------------------------------
FASTEST COMMANDER DEPLOYMENT SHOWCASE (Sim 4, Seat 2)
--------------------------------------------------------------------
  Cast Turn:     Turn 2 (Gold Keep, 7 cards)
  Opening Hand:  Caves of Koilos, Arcane Signet, Myrel, Shield of Argive, Martial Coup, Castle Ardenvale, Talisman of Conviction, Plains
  Deployment Sequence:
    T 1: Land: Caves of Koilos | Cast: Sol Ring | Cast: Arcane Signet
    T 2: Land: Plains | Cast: Talisman of Conviction | ** CAST Caesar, Legion's Emperor T2 **

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 79/80 (99%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T4.6
  Commander Cast Distribution:
    T 2: # (1)
    T 3: ########## (10)
    T 4: ################################# (33)
    T 5: ################### (19)
    T 6: ########## (10)
    T 7: ### (3)
    T 8: # (1)
    T 9: # (1)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   45/80 (56%)
    Silver Keep (Mana + Curve):          34/80 (42%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.95 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 75/80 (94%)
  Engine Readiness Avg:  T5.0
  Engine Readiness Distribution:
    T 3: #### (4)
    T 4: ############################ (28)
    T 5: ######################### (25)
    T 6: ############## (14)
    T 7: #### (4)
    T 8: ## (2)
    T 9: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 5.0, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
*   **Rules-Accurate Realism:** With the mana engine update deducting spent mana in real time and accounting for filter activation costs (Odyssey filter lands and Ravnica Signets requiring {1}), the false Turn 1 casts are eliminated.
*   **True Average Deployment:** Average deployment turn settles at **T4.6** (most frequent deployment turn is **Turn 4**, occurring in 41% of seats). T3 casts occur 12.5% of the time via a Turn 2 Talisman/Signet or Turn 1 Sol Ring.
*   **Fastest Deployment Provenance:** The single Turn 2 deployment out of 80 seats was verified as a pure rules-legal Sol Ring + Arcane Signet line from a Gold Keep hand (Sim 4, Seat 2).
*   **Stable Consistency:** 98% functional keeps (56% Gold, 42% Silver) and 94% Engine Readiness within the target window (avg T5.0). Perfect Bracket 3 compliance.
