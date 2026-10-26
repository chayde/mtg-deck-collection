---
deck_status: main
---

# Deck Guide: Obeka, Splitter of Seconds ("The Chronomancer's Courts")

## Commander Strategy
**[Obeka, Splitter of Seconds](https://scryfall.com/card/otj/222/obeka-splitter-of-seconds?utm_source=api)** ({1}{U}{B}{R})
*   **Archetype:** Grixis Combat-Triggered Upkeep Multiplier, Monarch Courts & Initiative Value Engine
*   **Bracket:** **Bracket 3 (Upgraded Casual)** | **1 / 3 Game Changers** ([**Fierce Guardianship**](https://scryfall.com/card/cmm/94/fierce-guardianship?utm_source=api))
*   **DTI Threat Index:** **40 / 96** (Solid Bracket 3, 32–51 band) | **Velocity:** `21 / 48` | **Suppression:** `15 / 40` | **All 4 Gatekeepers:** `PASSED (Safe)`
*   **DTI Reports:** [`dti_audit.md`](dti_audit.md) | [`dti_report.html`](dti_report.html) | **Goldfish Log:** [`GOLDFISH_LOG.md`](GOLDFISH_LOG.md)
*   **Core Goal:** Equip or enchant **Obeka, Splitter of Seconds** with unblockability, haste, power-scaling +1/+1 counters, or double strike so she deals combat damage to an opponent and triggers **2 to 8+ additional upkeep steps immediately after combat**. Convert that burst of post-combat upkeeps into an avalanche of triggers from all six Grixis **Monarch Courts**, the **Initiative (Undercity)**, **Extravagant Replication**, **Mechanized Production**, **Bonehoard Dracosaur**, and **Twilight Prophet** to drain out the table or win outright.

---

### ⏳ Deck Shape Geometry & The Post-Combat Upkeep Engine

Per [`DeckShapeReferenceGuide.md`](../../../DeckShapeReferenceGuide.md), **Obeka, Splitter of Seconds** ({1}{U}{B}{R}) is a **Shape 2 (Inverted Triangle / Hybrid T-Shape — Amplifier/Enabler)** commander:

1. **Command-Zone Upkeep Multiplier:**
   * Because Obeka sits in the Command Zone and converts every point of combat damage she deals to a player into an immediate post-combat upkeep step, the 99 cuts generic midrange filler and splits cleanly into two synergistic halves: **Combat Enablers/Scalers** (Haste, Unblockable, Double Strike, +1/+1 Rings) and **Upkeep/Time-Counter Payoffs** (Courts, Initiative, Suspend, Clones, and Drain).
2. **The M13 Ring Compounding Loop (*Ring of Valkas*, *Ring of Xathrid*, *Ring of Evos Isle*):**
   * Because Obeka is a 3-color ({U}{B}{R}) creature, all three M13 Rings recognize her color and put a `+1/+1` counter on her **at the beginning of every upkeep step**.
   * When Obeka connects for 2 damage, she creates 2 post-combat upkeeps—and the equipped Ring immediately puts two `+1/+1` counters on her during those post-combat upkeeps, turning her into a 4/7 for the next turn (or mid-turn if multiple Rings are attached) while granting Haste, `{2}` Regenerate, and `{2}` Hexproof.
3. **The Menace + *Silent Arbiter* Lock:**
   * Obeka has native **Menace** (*can't be blocked except by two or more creatures*), while **[Silent Arbiter](https://scryfall.com/card/cmm/972/silent-arbiter?utm_source=api)** ({4}) dictates that *no more than one creature can block each combat*. Together, **Silent Arbiter makes Obeka 100% unblockable** while restricting opponents to a single attacker per turn so they cannot easily steal your **Monarch** or **Initiative** crowns.
4. **One-Hit Undercity Completion (*Rilsa Rael, Kingpin*):**
   * The **Initiative** triggers at the beginning of each of your upkeeps. Connecting with Obeka for just 4 damage rockets you through the entire **Undercity** dungeon in a single post-combat phase—culminating in *Throne of the Dead Three* (reveal top 10 cards, put a creature onto the battlefield with three `+1/+1` counters and hexproof) and unlocking **Rilsa Rael**'s attack bonus (`+5/+0`, first strike, menace, and deathtouch) for future turns.

---

## 🛠️ Card Explanations

### 👑 Commander (1 Card)
*   **[Obeka, Splitter of Seconds](https://scryfall.com/card/otj/222/obeka-splitter-of-seconds?utm_source=api) ({1}{U}{B}{R}):** 2/5 Ogre Warlock with Menace that grants that many additional upkeep steps immediately after the combat phase whenever she deals combat damage to a player.

### 🌱 Ramp & Mana Acceleration (10 Cards)
*   **[Sol Ring](https://scryfall.com/card/msc/211/sol-ring?utm_source=api) ({1}):** Premier fast mana rock enabling Turn 2–3 Court or Obeka deployment.
*   **[Arcane Signet](https://scryfall.com/card/msc/191/arcane-signet?utm_source=api) ({2}):** Unconditional 2-mana untapped Grixis color fixer.
*   **[Talisman of Dominance](https://scryfall.com/card/msc/219/talisman-of-dominance?utm_source=api) ({2}):** Untapped 2-mana `{U}`/`{B}` rock.
*   **[Talisman of Indulgence](https://scryfall.com/card/msc/220/talisman-of-indulgence?utm_source=api) ({2}):** Untapped 2-mana `{B}`/`{R}` rock.
*   **[Talisman of Creativity](https://scryfall.com/card/frc/61/talisman-of-creativity?utm_source=api) ({2}):** Untapped 2-mana `{U}`/`{R}` rock.
*   **[Dimir Signet](https://scryfall.com/card/frc/56/dimir-signet?utm_source=api) ({2}):** 2-mana `{U}{B}` filter rock *(⚠️ Flagged in Deck Analysis for replacement per player non-Signet rule)*.
*   **[Izzet Signet](https://scryfall.com/card/frc/58/izzet-signet?utm_source=api) ({2}):** 2-mana `{U}{R}` filter rock *(⚠️ Flagged in Deck Analysis for replacement per player non-Signet rule)*.
*   **[Rakdos Signet](https://scryfall.com/card/frc/60/rakdos-signet?utm_source=api) ({2}):** 2-mana `{B}{R}` filter rock *(⚠️ Flagged in Deck Analysis for replacement per player non-Signet rule)*.
*   **[Nightscape Familiar](https://scryfall.com/card/dmr/94/nightscape-familiar?utm_source=api) ({1}{B}):** Reduces the cost of all Blue and Red spells (including **Obeka**) by `{1}` and regenerates for `{1}{B}` to hold back blockers.
*   **[Replicating Ring](https://scryfall.com/card/moc/372/replicating-ring?utm_source=api) ({3}):** Rainbow mana rock that accumulates night counters on every upkeep step—bursting into eight *Replicated Ring* tokens after just 1–2 Obeka combat hits (and immediately winning the game if enchanted with *Mechanized Production*!).

### ⚔️ Evasion, Haste, Pump & Combat Enablers (13 Cards)
*   **[Ring of Valkas](https://scryfall.com/card/cmr/469/ring-of-valkas?utm_source=api) ({2}):** Grants Haste (`Equip {1}`) and puts a `+1/+1` counter on Obeka at the beginning of every upkeep step.
*   **[Ring of Xathrid](https://scryfall.com/card/m13/215/ring-of-xathrid?utm_source=api) ({2}):** Grants `{2}: Regenerate` (`Equip {1}`) and puts a `+1/+1` counter on Obeka at the beginning of every upkeep step.
*   **[Ring of Evos Isle](https://scryfall.com/card/m13/211/ring-of-evos-isle?utm_source=api) ({2}):** Grants `{2}: Hexproof until end of turn` (`Equip {1}`) and puts a `+1/+1` counter on Obeka at the beginning of every upkeep step.
*   **[Lizard Blades](https://scryfall.com/card/neo/153/lizard-blades?utm_source=api) ({1}{R}):** Reconfigure `{2}` Equipment creature granting **Double Strike**—causing Obeka to deal combat damage twice (First Strike + Regular Damage) and doubling her post-combat upkeep triggers.
*   **[Brotherhood Regalia](https://scryfall.com/card/acr/71/brotherhood-regalia?utm_source=api) ({2}):** Premier evasion piece (`Equip legendary creature {1}`) granting **Unblockable** and **Ward {2}**.
*   **[Winged Boots](https://scryfall.com/card/otc/124/winged-boots?utm_source=api) ({1}{U}):** `Equip {1}` equipment granting **Flying** (combined with Obeka's native Menace) and a massive **Ward {4}** shield.
*   **[Trailblazer's Boots](https://scryfall.com/card/otc/269/trailblazers-boots?utm_source=api) ({2}):** Grants nonbasic landwalk (`Equip {2}`), making Obeka functionally unblockable in Commander pods.
*   **[Whispersilk Cloak](https://scryfall.com/card/msc/225/whispersilk-cloak?utm_source=api) ({3}):** Grants Unblockable and Shroud (`Equip {2}`) *(⚠️ See Shroud self-targeting note in Deck Analysis)*.
*   **[Swiftfoot Boots](https://scryfall.com/card/mbc/77/swiftfoot-boots?utm_source=api) ({2}):** Grants **Hexproof** and **Haste** (`Equip {1}`) while still allowing you to attach additional Rings and Auras to Obeka.
*   **[Lightning Greaves](https://scryfall.com/card/msc/202/lightning-greaves?utm_source=api) ({2}):** `Equip {0}` Haste and Shroud enabler.
*   **[Aqueous Form](https://scryfall.com/card/cmr/56/aqueous-form?utm_source=api) ({U}):** 1-mana Aura making Obeka unblockable and scrying 1 whenever she attacks.
*   **[Thassa, God of the Sea](https://scryfall.com/card/lcc/176/thassa-god-of-the-sea?utm_source=api) ({2}{U}):** Indestructible enchantment that scries 1 on every upkeep (filtering 3–6+ cards post-combat with Obeka) and pays `{1}{U}` to make Obeka unblockable.
*   **[Silent Arbiter](https://scryfall.com/card/cmm/972/silent-arbiter?utm_source=api) ({4}):** 1/5 artifact construct that restricts combat to 1 attacker and 1 blocker—making Menace creatures 100% unblockable while protecting your Monarch and Initiative status.

### 👑 Monarch Courts & The Initiative (7 Cards)
*   **[Rilsa Rael, Kingpin](https://scryfall.com/card/clb/293/rilsa-rael-kingpin?utm_source=api) ({3}{U}{B}):** Takes **The Initiative** on ETB (venturing into the *Undercity* on every upkeep) and, once a dungeon is completed, gives target attacker `+5/+0`, first strike, menace, and deathtouch on every attack.
*   **[Court of Vantress](https://scryfall.com/card/plst/WOC-22/court-of-vantress?utm_source=api) ({2}{U}{U}):** Takes the Monarch and creates a token copy of target artifact or enchantment (*Paradox Haze*, another Court, *Bonehoard Dracosaur* treasures, or *Ring of Valkas*) on every upkeep while you are the Monarch.
*   **[Court of Locthwain](https://scryfall.com/card/woc/23/court-of-locthwain?utm_source=api) ({2}{B}{B}):** Takes the Monarch and exiles the top card of an opponent's library on every upkeep, allowing you to cast one of those exiled cards **for free** during each upkeep while Monarch.
*   **[Court of Ambition](https://scryfall.com/card/cmr/114/court-of-ambition?utm_source=api) ({2}{B}{B}):** Takes the Monarch and forces each opponent to lose 6 life or discard 2 cards on every upkeep while Monarch (3 life or 1 card otherwise).
*   **[Court of Embereth](https://scryfall.com/card/plst/WOC-24/court-of-embereth?utm_source=api) ({2}{R}{R}):** Takes the Monarch, creates a 3/1 red Knight token on every upkeep, and deals damage equal to your creature count to each opponent on every upkeep while Monarch.
*   **[Court of Ire](https://scryfall.com/card/cmr/170/court-of-ire?utm_source=api) ({3}{R}{R}):** Takes the Monarch and deals 7 damage to any target on every upkeep while Monarch (2 damage otherwise).
*   **[Court of Cunning](https://scryfall.com/card/cmr/63/court-of-cunning?utm_source=api) ({1}{U}{U}):** Takes the Monarch and mills any number of target players for 10 cards on every upkeep while Monarch *(⚠️ Flagged in Deck Analysis as a swap candidate)*.

### 🔮 Upkeep Value, Clone, Drain & Token Engines (16 Cards)
*   **[Paradox Haze](https://scryfall.com/card/tsp/71/paradox-haze?utm_source=api) ({2}{U}):** Enchant player Aura granting an additional upkeep step after your first upkeep each turn (and prime clone target for *Court of Vantress* and *Extravagant Replication*).
*   **[Extravagant Replication](https://scryfall.com/card/fdn/154/extravagant-replication?utm_source=api) ({4}{U}{U}):** Creates a permanent token copy of another nonland permanent you control at the beginning of every upkeep step.
*   **[Mechanized Production](https://scryfall.com/card/mkc/109/mechanized-production?utm_source=api) ({2}{U}{U}):** Enchants an artifact you control to create a token copy every upkeep and **wins the game immediately** if you control 8 or more artifacts with the same name (pairs with *Replicating Ring*, *Generous Plunderer* Treasures, *Bonehoard Dracosaur* Treasures, or *Sol Ring*).
*   **[Bonehoard Dracosaur](https://scryfall.com/card/lci/134/bonehoard-dracosaur?utm_source=api) ({3}{R}{R}):** 5/5 Flying First Strike powerhouse that exiles the top 2 cards of your library on every upkeep (playable until end of turn) while creating 3/1 Dinosaurs and Treasure tokens.
*   **[Twilight Prophet](https://scryfall.com/card/mkc/143/twilight-prophet?utm_source=api) ({2}{B}{B}):** 2/4 Flying Vampire with Ascend; on every upkeep with the City's Blessing, reveals the top card of your library into your hand, drains each opponent for its mana value, and gains you that much life.
*   **[Plargg and Nassari](https://scryfall.com/card/soc/250/plargg-and-nassari?utm_source=api) ({3}{R}{R}):** Exiles a nonland spell from the top of all 4 libraries on every upkeep and lets you cast up to two of them **without paying their mana costs**.
*   **[Skyline Despot](https://scryfall.com/card/cmm/254/skyline-despot?utm_source=api) ({5}{R}{R}):** 5/5 Flying Dragon that makes you the Monarch on ETB and creates a 5/5 Flying Dragon token on every upkeep while you are the Monarch.
*   **[Dragonmaster Outcast](https://scryfall.com/card/tdc/211/dragonmaster-outcast?utm_source=api) ({R}):** 1-mana Shaman that creates a 5/5 Flying Dragon token on every upkeep once you control 6 or more lands.
*   **[Indulgent Tormentor](https://scryfall.com/card/ima/94/indulgent-tormentor?utm_source=api) ({3}{B}{B}):** 5/3 Flying Demon that draws you a card on every upkeep unless target opponent sacrifices a creature or pays 3 life.
*   **[Scrawling Crawler](https://scryfall.com/card/fdn/132/scrawling-crawler?utm_source=api) ({3}):** 3/2 Construct that makes each player draw a card on your upkeep and drains opponents for 1 life whenever they draw a card.
*   **[Phyrexian Arena](https://scryfall.com/card/fdn/180/phyrexian-arena?utm_source=api) ({1}{B}{B}):** Draws 1 card and loses 1 life at the beginning of every upkeep step.
*   **[Creeping Bloodsucker](https://scryfall.com/card/j25/415/creeping-bloodsucker?utm_source=api) ({1}{B}):** 2-mana Vampire that deals 1 damage to each opponent and gains you 3 life on every upkeep (completely offsetting life loss from *Phyrexian Arena* and *Talismans*).
*   **[Palace Siege](https://scryfall.com/card/c17/119/palace-siege?utm_source=api) ({3}{B}{B}):** Modal upkeep enchantment that either drains each opponent for 2 life (*Dragons*) or returns a creature card from your graveyard to hand (*Khans*) on every upkeep.
*   **[Generous Plunderer](https://scryfall.com/card/big/11/generous-plunderer?utm_source=api) ({1}{R}):** 2/2 Menace Rogue that creates an untapped Treasure for you (and a tapped Treasure for an opponent) on every upkeep and punishes artifact count on attack.
*   **[Venser's Journal](https://scryfall.com/card/c21/273/vensers-journal?utm_source=api) ({5}):** Grants unlimited hand size and gains 1 life per card in hand on every upkeep *(⚠️ Flagged in Deck Analysis as a swap candidate)*.
*   **[Alexios, Deimos of Kosmos](https://scryfall.com/card/acr/33/alexios-deimos-of-kosmos?utm_source=api) ({3}{R}):** 4/4 Trampler that untaps and gets a `+1/+1` counter at the beginning of *each player's* upkeep—meaning Obeka's post-combat upkeeps untap Alexios after combat and stack multiple `+1/+1` counters on him before he passes around the table.

### ⏳ Suspend & Time-Counter Engines (7 Cards)
*   **[As Foretold](https://scryfall.com/card/2x2/38/as-foretold?utm_source=api) ({2}{U}):** Puts a time counter on itself every upkeep and lets you cast a spell of mana value $\le X$ for `{0}` once each turn.
*   **[Jhoira of the Ghitu](https://scryfall.com/card/tsr/256/jhoira-of-the-ghitu?utm_source=api) ({1}{U}{R}):** Pays `{2}` to exile any nonland card from hand with 4 time counters and Suspend—allowing a single 4-damage Obeka swing to cast it immediately after combat for free.
*   **[Ancestral Vision](https://scryfall.com/card/tdc/144/ancestral-vision?utm_source=api) (`Suspend 4—{U}`):** 1-mana Suspend draw-3 spell that resolves immediately after combat when Obeka connects.
*   **[Profane Tutor](https://scryfall.com/card/mh2/97/profane-tutor?utm_source=api) (`Suspend 2—{1}{B}`):** Unconditional tutor that ticks off both time counters in a single 2-damage Obeka combat hit to find your missing win piece immediately.
*   **[Inspiring Refrain](https://scryfall.com/card/c21/27/inspiring-refrain?utm_source=api) ({4}{U}{U} / `Suspend 3—{2}{U}`):** Draws 2 cards and automatically re-exiles itself with 3 time counters—drawing 2 cards every 3 upkeeps for the rest of the game.
*   **[Rousing Refrain](https://scryfall.com/card/soc/253/rousing-refrain?utm_source=api) ({3}{R}{R} / `Suspend 3—{1}{R}`):** Adds `{R}` equal to an opponent's hand size (unlost through steps and phases until end of turn) and automatically re-suspends itself with 3 time counters—fueling massive post-combat main phases every 3 upkeeps.
*   **[Suspended Sentence](https://scryfall.com/card/dsc/25/suspended-sentence?utm_source=api) ({3}{B} / `Suspend 3—{1}{B}`):** Destroys an opposing creature, makes its controller lose 3 life, and re-suspends itself with 3 time counters for repeatable upkeep removal.

### 🛡️ Stack Shielding, Targeted Disruption & Sweepers (11 Cards — 1 Game Changer)
*   **[Fierce Guardianship](https://scryfall.com/card/cmm/94/fierce-guardianship?utm_source=api) ({2}{U}) [GAME CHANGER]:** Free noncreature counterspell while you control Obeka (`1 / 3` Game Changers).
*   **[Deflecting Swat](https://scryfall.com/card/cmm/214/deflecting-swat?utm_source=api) ({2}{R}):** Free target-redirection shield while you control Obeka.
*   **[Slip Out the Back](https://scryfall.com/card/clu/99/slip-out-the-back?utm_source=api) ({U}):** 1-mana instant that puts a `+1/+1` counter on Obeka (permanently increasing her extra upkeeps!) and phases her out along with all attached Equipment/Auras.
*   **[An Offer You Can't Refuse](https://scryfall.com/card/fdn/160/an-offer-you-cant-refuse?utm_source=api) ({U}):** 1-mana noncreature counterspell.
*   **[Counterspell](https://scryfall.com/card/dsc/114/counterspell?utm_source=api) ({U}{U}):** Unconditional 2-mana countermagic.
*   **[Arcane Denial](https://scryfall.com/card/msc/147/arcane-denial?utm_source=api) ({1}{U}):** Easy-to-cast `{1}{U}` unconditional counterspell whose delayed upkeep draw triggers on your very first post-combat upkeep if cast before/during combat!
*   **[Terminate](https://scryfall.com/card/msc/189/terminate?utm_source=api) ({B}{R}):** 2-mana instant creature destruction (no regeneration).
*   **[Feed the Swarm](https://scryfall.com/card/tle/257/feed-the-swarm?utm_source=api) ({1}{B}):** 2-mana creature or enchantment destruction in Black.
*   **[Chaos Warp](https://scryfall.com/card/mbc/72/chaos-warp?utm_source=api) ({2}{R}):** Instant-speed answer to any problematic permanent.
*   **[Toxic Deluge](https://scryfall.com/card/msc/161/toxic-deluge?utm_source=api) ({2}{B}):** Premier 3-mana scalable `-X/-X` board wipe; because Obeka has **5 toughness** (2/5), paying `X=3` or `X=4` frequently clears opposing boards while leaving Obeka alive!
*   **[Blasphemous Act](https://scryfall.com/card/msc/163/blasphemous-act?utm_source=api) ({8}{R}):** 1-mana emergency board reset.

### 🏔️ Lands (35 Cards — Baseline Mana Base)
*   **Triome & Rainbow Fixing (4):** **[Xander's Lounge](https://scryfall.com/card/snc/260/xanders-lounge?utm_source=api)**, **[Command Tower](https://scryfall.com/card/msc/233/command-tower?utm_source=api)**, **[Exotic Orchard](https://scryfall.com/card/mbc/79/exotic-orchard?utm_source=api)**, **[Crumbling Necropolis](https://scryfall.com/card/msc/237/crumbling-necropolis?utm_source=api)**.
*   **Fetch Lands (2):** **[Polluted Delta](https://scryfall.com/card/mh3/224/polluted-delta?utm_source=api)**, **[Bloodstained Mire](https://scryfall.com/card/mh3/216/bloodstained-mire?utm_source=api)**.
*   **Shock Lands (3):** **[Watery Grave](https://scryfall.com/card/trk/306/watery-grave?utm_source=api)**, **[Steam Vents](https://scryfall.com/card/trk/298/steam-vents?utm_source=api)**, **[Blood Crypt](https://scryfall.com/card/trk/278/blood-crypt?utm_source=api)**.
*   **Multiplayer Crowd Lands (3):** **[Morphic Pool](https://scryfall.com/card/clb/357/morphic-pool?utm_source=api)**, **[Training Center](https://scryfall.com/card/cmm/434/training-center?utm_source=api)**, **[Luxury Suite](https://scryfall.com/card/msc/252/luxury-suite?utm_source=api)**.
*   **Pain Lands (2):** **[Shivan Reef](https://scryfall.com/card/frc/83/shivan-reef?utm_source=api)**, **[Sulfurous Springs](https://scryfall.com/card/eoc/185/sulfurous-springs?utm_source=api)** *(Missing Underground River)*.
*   **Slow Lands (2):** **[Shipwreck Marsh](https://scryfall.com/card/fra/189/shipwreck-marsh?utm_source=api)**, **[Stormcarved Coast](https://scryfall.com/card/sos/263/stormcarved-coast?utm_source=api)** *(Missing Haunted Ridge)*.
*   **Check Lands (3):** **[Drowned Catacomb](https://scryfall.com/card/frc/69/drowned-catacomb?utm_source=api)**, **[Sulfur Falls](https://scryfall.com/card/frc/84/sulfur-falls?utm_source=api)**, **[Dragonskull Summit](https://scryfall.com/card/msc/238/dragonskull-summit?utm_source=api)**.
*   **Battle / Tango Land (1):** **[Sunken Hollow](https://scryfall.com/card/msc/271/sunken-hollow?utm_source=api)**.
*   **Utility Lands (2):** **[Rogue's Passage](https://scryfall.com/card/hoc/212/rogues-passage?utm_source=api)** (unblockable activation), **[Reliquary Tower](https://scryfall.com/card/soc/398/reliquary-tower?utm_source=api)** (no maximum hand size).
*   **Basic Lands (13):** **5 [Island](https://scryfall.com/card/trk/319/island?utm_source=api)**, **4 [Swamp](https://scryfall.com/card/trk/321/swamp?utm_source=api)**, **4 [Mountain](https://scryfall.com/card/trk/323/mountain?utm_source=api)**.

---

## 📊 Deck Analysis & Recommendations

### 1. Baseline Goldfish & DTI Telemetry Summary
*   **20-Game Goldfish Simulation (80 Seats — Bracket 3):**
    *   **Commander Cast Rate:** `79 / 80 (99%)` | **Average Cast Turn:** `Turn 4.7` (13 casts on T3, 35 casts on T4, 16 casts on T5, 15 delayed to T6–T10).
    *   **Opening Hand Quality:** `44% Gold Keeps` (35/80), `54% Silver Keeps` (43/80), `2% Desperation Keeps` (2/80), `6.90 avg starting hand size`.
    *   **Engine Readiness (Target $\le$ T7):** `69 / 80 (86%)` | **Average Engine Readiness:** `Turn 5.1` (`PASS`).
*   **DTI Power & Bracket Audit:**
    *   **DTI Threat Score:** `40 / 96` (Solid Bracket 3, 32–51 band).
    *   **Vectors:** **Velocity:** `21 / 48` (Safe, `< 28` threshold) | **Suppression:** `15 / 40` (Safe).
    *   **Gatekeepers:** All 4 Gatekeepers **PASSED (Safe)**.
    *   **Game Changers:** `1 / 3` (**Fierce Guardianship**; note that **Deflecting Swat** is not a Game Changer).

### 2. Core Structural Findings & Diagnostic Notes

1. **Player Preference Violation — 3 Filter Signets (*Rakdos Signet*, *Izzet Signet*, *Dimir Signet*):**
   * The baseline list includes all three Grixis filter Signets. Per repository rules against filter mana rocks (which cannot tap for `{1}` independently and caused a color-pip stall in Goldfish Sim 10 Seat 4), these 3 slots should be replaced with:
     * **[Fellwar Stone](https://scryfall.com/card/mbc/74/fellwar-stone?utm_source=api) ({2}):** Untapped multi-color rock with no filter requirement.
     * **[Midnight Clock](https://scryfall.com/card/otc/100/midnight-clock?utm_source=api) ({2}{U}):** Taps for `{U}` and puts an hour counter on itself at the beginning of **every upkeep** (including all of Obeka's post-combat extra upkeeps!), refilling your hand with a fresh 7 cards every 1–2 combat connections.
     * **[Sword of the Animist](https://scryfall.com/card/cmm/413/sword-of-the-animist?utm_source=api) ({2}):** Buffs Obeka by `+1/+1` (`+1` extra upkeep on every hit!) and ramps a basic land onto the battlefield on every attack.

2. **35-Land Count Bottleneck (35 Lands vs. 38 Template Target):**
   * While the quality of individual lands is excellent (Fetchlands, Shocklands, Crowd lands, Xander's Lounge), **35 total lands** is 3 lands below the 38-land Commander standard.
   * **Empirical Evidence from Goldfish Testing:** In 15 of 80 seats (`18.8%`), Obeka was delayed to Turn 6–10 (and failed to cast in Sim 10 Seat 4) due to missing the 4th or 5th land drop while holding 4–6 CMC Courts/Dragons and needing `{1}`–`{2}` mana to equip boots.
   * **Recommended Fix (+3 Lands $\rightarrow$ 38 Lands):**
     * Add **[Underground River](https://scryfall.com/card/frc/87/underground-river?utm_source=api)** (completes the untapped Painland trio alongside *Shivan Reef* and *Sulfurous Springs*).
     * Add **[Haunted Ridge](https://scryfall.com/card/fra/180/haunted-ridge?utm_source=api)** (completes the Slowland trio alongside *Shipwreck Marsh* and *Stormcarved Coast*).
     * Add **+1 Basic [Swamp](https://scryfall.com/card/trk/321/swamp?utm_source=api)** (or **[Island](https://scryfall.com/card/trk/319/island?utm_source=api)**) to bring Basic Lands to 14 and total lands to **38**.

3. **Shroud Self-Targeting Conflict (*Whispersilk Cloak* & *Lightning Greaves*):**
   * The deck runs 8 Equipment and Auras that want to stack onto Obeka simultaneously (**Ring of Valkas**, **Ring of Xathrid**, **Ring of Evos Isle**, **Lizard Blades**, **Brotherhood Regalia**, **Winged Boots**, **Trailblazer's Boots**, **Aqueous Form**).
   * Because **Shroud** prevents *you* from targeting Obeka with your own Equip/Reconfigure/Aura abilities, attaching **[Whispersilk Cloak](https://scryfall.com/card/msc/225/whispersilk-cloak?utm_source=api)** ({3}, `Equip {2}`) locks out your +1/+1 Rings and *Lizard Blades* unless you control a second creature and pay `{2}` to move Cloak off and `{2}` to move it back. Since you already run **Brotherhood Regalia**, **Winged Boots**, **Swiftfoot Boots**, **Trailblazer's Boots**, **Aqueous Form**, **Thassa, God of the Sea**, **Silent Arbiter**, and **Rogue's Passage**, *Whispersilk Cloak* is the cleanest cut for a land or high-synergy upgrade.

4. **Weakest Payoff Slots to Cut for Lands / Upgrades:**
   * **[Venser's Journal](https://scryfall.com/card/c21/273/vensers-journal?utm_source=api) ({5}):** At 5 mana, pure lifegain does not advance your board state, card velocity, or clock, and *Creeping Bloodsucker* + *Twilight Prophet* + *Palace Siege* already buffer your life total at lower mana investment.
   * **[Court of Cunning](https://scryfall.com/card/cmr/63/court-of-cunning?utm_source=api) ({1}{U}{U}):** Milling opponents for 2 or 10 cards per upkeep without a graveyard-hate or reanimator package frequently fuels opposing graveyard strategies before milling 250+ cards across 3 opponents.
   * **[Jhoira of the Ghitu](https://scryfall.com/card/tsr/256/jhoira-of-the-ghitu?utm_source=api) ({1}{U}{R}):** Because your average mana value is already lean and only 2 cards in the 99 cost 6+ mana (*Extravagant Replication*, *Skyline Despot*), paying `{2}` to exile cards face-up for 4 time counters is often slower than simply casting them with *As Foretold* or *Rousing Refrain*.

---

## 🚀 Future Roadmap: Upgrades & Considerations

### 💡 High-Impact Tech to Consider
*   **[Caves of Chaos Adventurer](https://scryfall.com/card/clb/167/caves-of-chaos-adventurer?utm_source=api) ({3}{R}):** Second **Initiative** enabler alongside *Rilsa Rael, Kingpin*. Because Obeka finishes the entire *Undercity* in a single 4-damage combat hit, doubling your Initiative density gives you a 1-turn path to *Throne of the Dead Three* and free spells on attack.
*   **[Shadow of the Second Sun](https://scryfall.com/card/mh3/70/shadow-of-the-second-sun?utm_source=api) ({4}{U}{U}):** Enchants you to grant an entire additional **Beginning Phase (Untap + Upkeep + Draw)** after your postcombat main phase—untapping all your lands and creatures after combat while adding another upkeep and draw step every turn.
*   **[Descent into Avernus](https://scryfall.com/card/clb/169/descent-into-avernus?utm_source=api) ({2}{R}):** Scales by +2 descent counters on every upkeep step—turning a single 3-upkeep Obeka connection into `2 + 4 + 6 = 12 Treasures` and `12 damage` to each player (while your *Creeping Bloodsucker* / *Twilight Prophet* / *Palace Siege* lifegain breaks parity).
*   **[The Ninth Doctor](https://scryfall.com/card/who/148/the-ninth-doctor?utm_source=api) ({1}{U}{R}):** 2/4 Haste creature that grants an additional upkeep step whenever he untaps during your untap step (and triggers again if you run *Shadow of the Second Sun* or *Sphinx of the Second Sun*).

### 🛒 Active Acquisition List (Recommended Phase 1 Swaps)
*These 6 swaps resolve the 3 filter Signets and 35-land deficit while preserving all core upkeep engines:*

| **New Card (In)** | **Card to Remove (Out)** | **Category** | **Status** |
| :--- | :--- | :--- | :--- |
| **[Fellwar Stone](https://scryfall.com/card/mbc/74/fellwar-stone?utm_source=api)** | Dimir Signet | Ramp (Non-Filter) | Recommended |
| **[Midnight Clock](https://scryfall.com/card/otc/100/midnight-clock?utm_source=api)** | Izzet Signet | Ramp + Upkeep Draw-7 | Recommended |
| **[Sword of the Animist](https://scryfall.com/card/cmm/413/sword-of-the-animist?utm_source=api)** | Rakdos Signet | Ramp + Obeka +1/+1 | Recommended |
| **[Underground River](https://scryfall.com/card/frc/87/underground-river?utm_source=api)** | Venser's Journal | Land #36 (UB Painland) | Recommended |
| **[Haunted Ridge](https://scryfall.com/card/fra/180/haunted-ridge?utm_source=api)** | Court of Cunning | Land #37 (BR Slowland) | Recommended |
| **[Swamp](https://scryfall.com/card/trk/321/swamp?utm_source=api)** (or **[Caves of Chaos Adventurer](https://scryfall.com/card/clb/167/caves-of-chaos-adventurer?utm_source=api)**) | Whispersilk Cloak | Land #38 / Initiative | Recommended |

---

## 📜 Deck Changelog
*   **[2026-10-26]:** Initial 100-card baseline deck creation from candidate list ("The Chronomancer's Courts"), comprehensive architectural & mechanical audit, 20-game Goldfish simulation (99% cast rate, T4.7 avg cast, 86% T<=7 Engine Readiness, T5.1 avg), DTI power evaluation (40 / 96 Bracket 3, Velocity 21/48, Suppression 15/40, 1/3 Game Changers, All Gates Passed), and MTG Forge synchronization.

---

## 🃏 Plain Text Copy/Paste (Moxfield Import)
COMMANDER:  
1 Obeka, Splitter of Seconds  

DECK:  
1 Alexios, Deimos of Kosmos  
1 An Offer You Can't Refuse  
1 Ancestral Vision  
1 Aqueous Form  
1 Arcane Denial  
1 Arcane Signet  
1 As Foretold  
1 Blasphemous Act  
1 Blood Crypt  
1 Bloodstained Mire  
1 Bonehoard Dracosaur  
1 Brotherhood Regalia  
1 Chaos Warp  
1 Command Tower  
1 Counterspell  
1 Court of Ambition  
1 Court of Cunning  
1 Court of Embereth  
1 Court of Ire  
1 Court of Locthwain  
1 Court of Vantress  
1 Creeping Bloodsucker  
1 Crumbling Necropolis  
1 Deflecting Swat  
1 Dimir Signet  
1 Dragonmaster Outcast  
1 Dragonskull Summit  
1 Drowned Catacomb  
1 Exotic Orchard  
1 Extravagant Replication  
1 Feed the Swarm  
1 Fierce Guardianship  
1 Generous Plunderer  
1 Indulgent Tormentor  
1 Inspiring Refrain  
5 Island  
1 Izzet Signet  
1 Jhoira of the Ghitu  
1 Lightning Greaves  
1 Lizard Blades  
1 Luxury Suite  
1 Mechanized Production  
1 Morphic Pool  
4 Mountain  
1 Nightscape Familiar  
1 Palace Siege  
1 Paradox Haze  
1 Phyrexian Arena  
1 Plargg and Nassari  
1 Polluted Delta  
1 Profane Tutor  
1 Rakdos Signet  
1 Reliquary Tower  
1 Replicating Ring  
1 Rilsa Rael, Kingpin  
1 Ring of Evos Isle  
1 Ring of Valkas  
1 Ring of Xathrid  
1 Rogue's Passage  
1 Rousing Refrain  
1 Scrawling Crawler  
1 Shipwreck Marsh  
1 Shivan Reef  
1 Silent Arbiter  
1 Skyline Despot  
1 Slip Out the Back  
1 Sol Ring  
1 Steam Vents  
1 Stormcarved Coast  
1 Sulfur Falls  
1 Sulfurous Springs  
1 Sunken Hollow  
1 Suspended Sentence  
4 Swamp  
1 Swiftfoot Boots  
1 Talisman of Creativity  
1 Talisman of Dominance  
1 Talisman of Indulgence  
1 Terminate  
1 Thassa, God of the Sea  
1 Toxic Deluge  
1 Trailblazer's Boots  
1 Training Center  
1 Twilight Prophet  
1 Venser's Journal  
1 Watery Grave  
1 Whispersilk Cloak  
1 Winged Boots  
1 Xander's Lounge  
