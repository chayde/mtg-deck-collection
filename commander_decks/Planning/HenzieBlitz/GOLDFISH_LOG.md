# Goldfish Simulation Log: Henzie "Toolbox" Torre

## 2026-09-03 — Board Wipe Optimization: Incinerator of the Guilty In, Blasphemous Act Out (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 77/80 (96%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.8
  Commander Cast Distribution:
    T 2: ################### (19)
    T 3: ######################## (24)
    T 4: ############# (13)
    T 5: ########## (10)
    T 6: ### (3)
    T 7: #### (4)
    T 8: # (1)
    T 9: # (1)
    T10: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   22/80 (28%)
    Silver Keep (Mana + Curve):          56/80 (70%)
    Desperation Keep (Mulligan to <=5):   2/80 (2%)
    Average Starting Hand Size:          6.86 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 72/80 (90%)  ← All-time high 90%!
  Engine Readiness Avg:  T4.5
  Engine Readiness Distribution:
    T 3: ################## (18)
    T 4: ############################# (29)
    T 5: ################ (16)
    T 6: ##### (5)
    T 7: #### (4)
    T 8: # (1)
    T 9: # (1)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.5, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced noncreature symmetrical sweeper *Blasphemous Act* ({8}{R}) with blitzable 6/6 flying/trample dragon *Incinerator of the Guilty* ({4}{R}{R}).
- Breaks parity by wiping opposing creatures/planeswalkers on combat damage via collect evidence while leaving our board and mana dorks completely intact.
- Searchable with *Survival of the Fittest* / *Fauna Shaman*.
- Achieved an all-time peak **90% Target Window Readiness Rate (72/80 hands)**!
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-09-03 — Engine Velocity Refinement: Birthing Ritual In, Eternal Witness Out (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 77/80 (96%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T4.1
  Commander Cast Distribution:
    T 2: ################## (18)
    T 3: ######################### (25)
    T 4: ######### (9)
    T 5: ####### (7)
    T 6: ####### (7)
    T 7: #### (4)
    T 8: ## (2)
    T 9: #### (4)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   27/80 (34%)
    Silver Keep (Mana + Curve):          52/80 (65%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.90 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 68/80 (85%)
  Engine Readiness Avg:  T4.8
  Engine Readiness Distribution:
    T 2: # (1)
    T 3: ################ (16)
    T 4: ########################## (26)
    T 5: ############## (14)
    T 6: ####### (7)
    T 7: #### (4)
    T 8: ## (2)
    T 9: ##### (5)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.8, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced non-blitzable *Eternal Witness* ({1}{G}{G}) with 2-mana repeatable sacrifice engine *Birthing Ritual* ({1}{G}).
- Retained *Timeless Witness* ({3}{G}) as the primary recursion creature (blitzable for 3 mana with haste, card draw, and Eternalize).
- Commander cast rate reached **96%** (77/80 hands).
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-09-02 — Strixhaven Adventure Creature Integration (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 75/80 (94%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.5  ← All-time personal best!
  Commander Cast Distribution:
    T 2: ########################## (26)
    T 3: #################### (20)
    T 4: ############### (15)
    T 5: ####### (7)
    T 6: ### (3)
    T 7: # (1)
    T 8: # (1)
    T 9: # (1)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   26/80 (32%)
    Silver Keep (Mana + Curve):          54/80 (68%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)  ← Flawless keep rate!
    Average Starting Hand Size:          6.99 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 70/80 (88%)
  Engine Readiness Avg:  T4.4
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ##################### (21)
    T 4: ######################### (25)
    T 5: ################# (17)
    T 6: #### (4)
    T 7: # (1)
    T 8: ## (2)
    T 9: ## (2)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced standalone *Demonic Tutor* and *Reanimate* with Strixhaven Adventure creatures: *Emeritus of Woe* ({3}{B} // {1}{B}) and *Grave Researcher* ({2}{B} // {B}).
- Drops official Game Changers to just **1 / 3** ([*Survival of the Fittest*]).
- Recorded **0% desperation keeps** with an average starting hand size of **6.99 cards**.
- Commander cast average reached an all-time fastest **Turn 3.5**.
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-09-02 — Budget Land Tuning: Boseiju Out, 4th Forest In (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 76/80 (95%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.7
  Commander Cast Distribution:
    T 2: ############################ (28)  ← 35% of games hit Turn 2 Henzie!
    T 3: ################ (16)
    T 4: ############ (12)
    T 5: ######## (8)
    T 6: ##### (5)
    T 7: ### (3)
    T 9: # (1)
    T10: ### (3)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   31/80 (39%)
    Silver Keep (Mana + Curve):          46/80 (57%)
    Desperation Keep (Mulligan to <=5):   3/80 (4%)
    Average Starting Hand Size:          6.89 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.5
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ###################### (22)
    T 4: ####################### (23)
    T 5: ############## (14)
    T 6: ####### (7)
    T 7: ### (3)
    T 9: # (1)
    T10: #### (4)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.5, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced *Boseiju, Who Endures* with a 4th basic *Forest*.
- Paper acquisition cost reduced by ~$55.
- Increased green basic consistency yielded an all-time high of **28 Turn 2 Henzie deployments (35%)** and 95% total cast rate.
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-09-02 — Creature Suite Overhaul & Velocity Optimization (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 74/80 (92%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.7
  Commander Cast Distribution:
    T 2: ##################### (21)
    T 3: ####################### (23)
    T 4: ############ (12)
    T 5: ####### (7)
    T 6: ###### (6)
    T 7: ## (2)
    T 8: # (1)
    T 9: # (1)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   32/80 (40%)
    Silver Keep (Mana + Curve):          47/80 (59%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.96 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.4
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ##################### (21)
    T 4: ###################### (22)
    T 5: ################# (17)
    T 6: ###### (6)
    T 7: ### (3)
    T 8: # (1)
    T 9: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced *Kardur, Doomscourge*, *Atsushi, the Blazing Sky*, *Disciple of Bolas*, and *Chaos Warp* with *Sowing Mycospawn*, *Necron Deathmark*, *Damage Control Crew*, and *Maha, Its Feathers Night*.
- Kept protected favorites *Timeless Witness* and *Eternal Witness*.
- Target Window Readiness hit a new high of **89%** (71/80) with an average engine turn of **T4.4**.
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-09-02 — Acceleration, Free Interaction & Reanimation Integration (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 75/80 (94%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.6 (Fastest deployment speed to date!)
  Commander Cast Distribution:
    T 2: ######################## (24)
    T 3: #################### (20)
    T 4: ############## (14)
    T 5: ######## (8)
    T 6: #### (4)
    T 7: # (1)
    T 8: # (1)
    T 9: ## (2)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   32/80 (40%)
    Silver Keep (Mana + Curve):          47/80 (59%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.90 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 69/80 (86%)
  Engine Readiness Avg:  T4.6
  Engine Readiness Distribution:
    T 2: ### (3)
    T 3: ################ (16)
    T 4: ######################### (25)
    T 5: ################## (18)
    T 6: ##### (5)
    T 7: ## (2)
    T 8: # (1)
    T 9: #### (4)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.6, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced *Orcish Lumberjack* with *Utopia Sprawl*, *Tibalt's Trickery* with *Deadly Rollick*, and *Birthing Ritual* with *Will of the Abzan*.
- Commander average cast time reached a new personal best of **Turn 3.6** with 24 Turn 2 casts.
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-09-01 — Windgrace's Judgment Integration (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 75/80 (94%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.7
  Commander Cast Distribution:
    T 2: ##################### (21)
    T 3: ##################### (21)
    T 4: ################## (18)
    T 5: ### (3)
    T 6: ###### (6)
    T 7: ## (2)
    T 8: ### (3)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   35/80 (44%)
    Silver Keep (Mana + Curve):          44/80 (55%)
    Desperation Keep (Mulligan to <=5):   1/80 (1%)
    Average Starting Hand Size:          6.95 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 70/80 (88%)
  Engine Readiness Avg:  T4.4
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ##################### (21)
    T 4: ######################### (25)
    T 5: ############# (13)
    T 6: ####### (7)
    T 7: ## (2)
    T 8: ### (3)
    T 9: # (1)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.4, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced *Beast Within* with *Windgrace's Judgment*.
- Eliminates 3/3 beast token donation in favor of instant-speed 3-for-1 permanent removal.
- Engine readiness avg clocked in at T4.4 (88% target window readiness).
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-09-01 — Velocity & Graveyard Hate Refinement (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 77/80 (96%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.8
  Commander Cast Distribution:
    T 2: ####################### (23)
    T 3: ######################## (24)
    T 4: ########### (11)
    T 5: ####### (7)
    T 6: #### (4)
    T 7: # (1)
    T 8: ## (2)
    T 9: ### (3)
    T10: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   31/80 (39%)
    Silver Keep (Mana + Curve):          49/80 (61%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.94 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 70/80 (88%)
  Engine Readiness Avg:  T4.6
  Engine Readiness Distribution:
    T 2: ### (3)
    T 3: ###################### (22)
    T 4: #################### (20)
    T 5: ################ (16)
    T 6: ####### (7)
    T 7: ## (2)
    T 8: ## (2)
    T 9: ### (3)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.6, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced *Etali, Primal Conqueror*, *Rampant Rejuvenator*, and *Gray Merchant of Asphodel* with *Gwenom, Remorseless*, *Author of Shadows*, and *Flare of Cultivation*.
- Commander cast rate improved to 96% (77/80) with 0% desperation keeps.
- Target window engine readiness sits at 88% (T4.6 average).
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-08-31 — Bringer of the Last Gift Integration (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 75/80 (94%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.7
  Commander Cast Distribution:
    T 2: ####################### (23)
    T 3: ######################### (25)
    T 4: ######## (8)
    T 5: ####### (7)
    T 6: ##### (5)
    T 7: ## (2)
    T 8: # (1)
    T 9: ## (2)
    T10: ## (2)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   36/80 (45%)
    Silver Keep (Mana + Curve):          44/80 (55%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.96 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 67/80 (84%)
  Engine Readiness Avg:  T4.6
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ####################### (23)
    T 4: #################### (20)
    T 5: ############# (13)
    T 6: ####### (7)
    T 7: ## (2)
    T 8: ## (2)
    T 9: #### (4)
    T10: ## (2)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.6, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- Replaced *Treeshaker Chimera* with *Bringer of the Last Gift*.
- Gold keep rate increased to 45% with 0% desperation keeps (average starting hand size 6.96).
- T2 commander casts increased to 23 (averaging T3.7 cast turn).
- Bracket compliance remains PASS for Bracket 3.

---

## 2026-08-31 — Bracket 3 Overhaul Validation (20 sims, 10 turns, Bracket 3)

**Command:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/HenzieBlitz/moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

**Results:**
```
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: Henzie "Toolbox" Torre (CMC 3)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 76/80 (95%)
  Commander Cast Range: T2 - T10
  Commander Cast Avg:   T3.9
  Commander Cast Distribution:
    T 2: ################ (16)
    T 3: ############################# (29)
    T 4: ########## (10)
    T 5: ########## (10)
    T 6: # (1)
    T 7: ##### (5)
    T 8: ## (2)
    T 9: ## (2)
    T10: # (1)

  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   32/80 (40%)
    Silver Keep (Mana + Curve):          46/80 (57%)
    Desperation Keep (Mulligan to <=5):   2/80 (2%)
    Average Starting Hand Size:          6.90 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 71/80 (89%)
  Engine Readiness Avg:  T4.6
  Engine Readiness Distribution:
    T 2: ## (2)
    T 3: ############### (15)
    T 4: ############################## (30)
    T 5: ############## (14)
    T 6: ##### (5)
    T 7: ##### (5)
    T 8: ## (2)
    T 9: ## (2)
    T10: # (1)

  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck deploys its engine around Turn 4.6, perfectly positioned to execute and threaten a win on Bracket 3 (Upgraded)'s target (Turn 7+).
```

**Notes:**
- High 1-drop dork density enabled frequent Turn 2 Henzie deployments and consistent Turn 3/4 Blitz cadence.
- 89% of simulated hands achieved full Engine Readiness on or before Turn 7 (average Turn 4.6), comfortably passing Bracket 3 compliance.
- 97% combined Gold and Silver opening hand keep rate with a 6.90 card average starting hand.
