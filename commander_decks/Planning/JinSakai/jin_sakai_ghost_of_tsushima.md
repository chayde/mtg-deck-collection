---
deck_status: main
---

# Deck Guide: Jin Sakai, Ghost of Tsushima ("The Three-Front Standoff")

## Commander Strategy
**[Jin Sakai, Ghost of Tsushima](https://scryfall.com/card/sld/2226/jin-sakai-ghost-of-tsushima?utm_source=api)** ({1}{W}{U}{B})
*   **Archetype:** Esper Three-Front Saboteur Control & Double-Strike Value Engine
*   **Bracket:** **Bracket 3 (Low Bracket 3 — Upgraded Casual)** | **0 / 3 Game Changers**
*   **DTI Threat Index:** **33 / 96** (Low Bracket 3, 32–51 band) | **Velocity:** `16 / 48` | **Suppression:** `15 / 40` | **All 4 Gatekeepers:** `PASSED (Safe)`
*   **DTI Reports:** [`dti_audit.md`](dti_audit.md) | [`dti_report.html`](dti_report.html) | **Goldfish Log:** [`GOLDFISH_LOG.md`](GOLDFISH_LOG.md)
*   **Core Goal:** Exploit Jin Sakai's per-player solo attack trigger across all 3 opponents simultaneously, granting up to three Saboteur creatures per combat either **Ghost** (`can't be blocked`) to guarantee combat-damage triggers or **Standoff** (`double strike`) to trigger them twice. Convert massive card velocity and Treasure generation into lethal life-halving strikes (*Virtus the Veiled*, *Quietus Spike*), one-hit eliminations (*Vorpal Sword*), or team-wide double-strike overruns (*Akroma's Will*, *True Conviction*, *Odric, Lunarch Marshal*).

---

### 🏯 Deck Shape Geometry & The Three-Front Standoff Engine

Per [`DeckShapeReferenceGuide.md`](../../../DeckShapeReferenceGuide.md), **Jin Sakai, Ghost of Tsushima** ({1}{W}{U}{B}) is a hybrid **Shape 2 (Inverted Triangle — Amplifier)** and **Shape 4 (Pillar-Shifted — Card Advantage Gainer)** commander:

1. **The 3-Player Solo Attack Loophole:**
   * Jin Sakai's second trigger reads: *"Whenever a creature you control attacks a player, if no other creatures are attacking **that player**, choose one — **Standoff** (It gains double strike until end of turn) or **Ghost** (It can't be blocked this turn)."*
   * Because it checks *per defending player*, attacking **Opponent A with Creature 1**, **Opponent B with Creature 2**, and **Opponent C with Creature 3** triggers Jin Sakai **three separate times every combat step**.
2. **Applying the Commander Subtraction Principle (Zero Vanilla 1/1 Unblockables):**
   * Because Jin Sakai already provides unconditional unblockability (**Ghost**) and card draw in the Command Zone, this deck cuts all vanilla 1/1 unblockable dorks (*Slither Blade*, *Triton Shorestalker*, *Mist-Cloaked Herald*) and redundant evasion auras (*Aqueous Form*).
   * Instead, every attacker in the 99 is a **Saboteur** with a high-impact `"Whenever ~ deals combat damage to a player"` trigger. If an opponent has blockers, **Ghost** guarantees the trigger fires; if an opponent is open (or your creature already has flying/protection), **Standoff** gives it **Double Strike** so its trigger fires **twice**!
3. **The First-Strike Ninjutsu Double-Dip (CR 510.4):**
   * Normally, bouncing an attacker with Ninjutsu before damage wastes attack triggers. However, when Jin Sakai grants an unblocked Saboteur **Standoff (Double Strike)**, it deals **First Strike combat damage** first (resolving its combat-damage trigger). Then, still inside combat *before* the Regular Combat Damage step, you can activate **Ninjutsu** (*Fallen Shinobi*, *Yuriko, the Tiger's Shadow*, *Mist-Syndicate Naga*, *Kaito, Bane of Nightmares*)—returning the first creature to hand while the Ninja enters tapped and attacking to deal **Regular Combat Damage** in the exact same combat!

---

## 🛠️ Card Explanations

### 👑 Commander (1 Card)
*   **[Jin Sakai, Ghost of Tsushima](https://scryfall.com/card/sld/2226/jin-sakai-ghost-of-tsushima?utm_source=api) ({1}{W}{U}{B}):** 2/4 Human Samurai that draws a card on combat damage (2 cards when he gives himself *Standoff*) and grants up to 3 solo attackers per combat either *Standoff* (Double Strike) or *Ghost* (Unblockable).

### 🌱 Ramp & Treasure Velocity (11 Cards — Zero Filter Rocks)
*   **[Sol Ring](https://scryfall.com/card/msc/211/sol-ring?utm_source=api) ({1}):** Premier Turn 1 mana acceleration enabling Turn 2–3 Jin Sakai deployment.
*   **[Wayfarer's Bauble](https://scryfall.com/card/hoc/211/wayfarers-bauble?utm_source=api) ({1}):** Curves Turn 1 Bauble into Turn 2 basic land ramp to fix Esper colors without green.
*   **[Arcane Signet](https://scryfall.com/search?q=!"Arcane+Signet") ({2}):** Unconditional untapped Esper mana rock.
*   **[Fellwar Stone](https://scryfall.com/card/mbc/74/fellwar-stone?utm_source=api) ({2}):** 2-mana untapped multi-color rock.
*   **[Talisman of Dominance](https://scryfall.com/card/msc/219/talisman-of-dominance?utm_source=api) ({2}):** Immediate untapped {U}/{B} mana rock (replaces filter Signets).
*   **[Talisman of Progress](https://scryfall.com/card/msc/221/talisman-of-progress?utm_source=api) ({2}):** Immediate untapped {W}/{U} mana rock.
*   **[Talisman of Hierarchy](https://scryfall.com/card/soc/358/talisman-of-hierarchy?utm_source=api) ({2}):** Immediate untapped {W}/{B} mana rock.
*   **[Ornithopter of Paradise](https://scryfall.com/card/cmm/966/ornithopter-of-paradise?utm_source=api) ({2}):** 0/2 flying rainbow mana dork that can also carry equipment or swing solo with *Ghost*/*Standoff* in an emergency.
*   **[Lotho, Corrupt Shirriff](https://scryfall.com/card/ltr/213/lotho-corrupt-shirriff?utm_source=api) ({W}{B}):** Generates a Treasure token whenever any player casts their second spell each turn.
*   **[Loyal Warhound](https://scryfall.com/card/afr/23/loyal-warhound?utm_source=api) ({1}{W}):** 3/1 Vigilance catch-up Plains ramp creature that immediately serves as a solo attacker for Jin Sakai.
*   **[Sword of the Animist](https://scryfall.com/card/cmm/413/sword-of-the-animist?utm_source=api) ({2}):** Repeatable basic land ramp on every attack while buffing a solo attacker by +1/+1.

### 🧠 Card Advantage & Combat Draw Multipliers (10 Cards)
*   **[Baleful Strix](https://scryfall.com/search?q=!"Baleful+Strix") ({U}{B}):** Replaces itself on ETB and provides a 1/1 Flying Deathtouch body; when given *Standoff* (Double Strike), it slays any blocker in First Strike before taking damage.
*   **[Satoru, the Infiltrator](https://scryfall.com/card/otj/230/satoru-the-infiltrator?utm_source=api) ({U}{B}):** 2/3 Menace body that draws a card whenever a nontoken creature enters via Ninjutsu without mana spent to cast it.
*   **[Malcolm, Alluring Scoundrel](https://scryfall.com/card/lci/63/malcolm-alluring-scoundrel?utm_source=api) ({1}{U}):** 2/1 Flash Flyer; with *Standoff* (Double Strike), puts 2 chorus counters on itself per combat and loots twice—reaching the 4-counter free-spell threshold in just two attacks.
*   **[Dimir Cutpurse](https://scryfall.com/card/ddh/49/dimir-cutpurse?utm_source=api) ({1}{U}{B}):** Forces the defending player to discard a card and draws you a card on hit—yielding a 4-card swing (draw 2, discard 2) with Double Strike.
*   **[Tymna the Weaver](https://scryfall.com/card/c16/48/tymna-the-weaver?utm_source=api) ({1}{W}{B}):** 2/2 Lifelink; because Jin Sakai naturally splits attacks across all 3 opponents, Tymna reliably draws 3 cards every postcombat main phase.
*   **[Breena, the Demagogue](https://scryfall.com/card/soc/298/breena-the-demagogue?utm_source=api) ({1}{W}{B}):** 1/3 Flyer that rewards attacking multiple opponents by drawing cards and putting two +1/+1 counters on a solo Double Strike attacker before damage.
*   **[Gix, Yawgmoth Praetor](https://scryfall.com/card/tdc/181/gix-yawgmoth-praetor?utm_source=api) ({1}{B}{B}):** Turns every combat damage hit into a card draw (twice per Double Strike attacker) and provides a late-game 7-mana mass heist outlet.
*   **[Reconnaissance Mission](https://scryfall.com/card/msc/153/reconnaissance-mission?utm_source=api) ({2}{U}{U}):** Draws a card on every combat damage hit—triggering twice for each Double Strike attacker across all 3 opponents.
*   **[Bident of Thassa](https://scryfall.com/card/lcc/146/bident-of-thassa?utm_source=api) ({2}{U}{U}):** Draws a card on every combat damage hit and can force opponents' creatures to tap out and attack so their shields are down for *Standoff* (Double Strike) on your turn.
*   **[Enduring Curiosity](https://scryfall.com/card/dsk/51/enduring-curiosity?utm_source=api) ({2}{U}{U}):** 4/3 Flash Cat Glimmer that draws on every combat damage hit and returns as a non-creature enchantment if destroyed.

### 🥷 Saboteur & First-Strike Ninjutsu Engines (17 Cards)
*   **[Daxos of Meletis](https://scryfall.com/card/ncc/335/daxos-of-meletis?utm_source=api) ({1}{W}{U}):** Evades power $\ge 3$ blockers, gains life, and exiles the top card of the defending player's library to cast (exiling 2 cards with Double Strike).
*   **[Thief of Sanity](https://scryfall.com/card/otc/243/thief-of-sanity?utm_source=api) ({1}{U}{B}):** 2/2 Flyer that looks at the top 3 cards of an opponent's library and steals the best card face down—stealing 2 spells per swing with *Standoff* Double Strike.
*   **[Cephalid Constable](https://scryfall.com/card/10e/72/cephalid-constable?utm_source=api) ({1}{U}{U}):** The ultimate Jin Sakai secret weapon: bounces permanents (including lands) equal to the combat damage it deals. Unblockable or Double Strike (especially with counters from Breena/Raffine/Drana) bounces 2 to 6+ permanents in a single swing.
*   **[Raffine, Scheming Seer](https://scryfall.com/card/snc/213/raffine-scheming-seer?utm_source=api) ({W}{U}{B}):** 1/4 Flying Ward {1}; Connives X on attack, filtering your hand and growing a Double Strike attacker before First Strike damage.
*   **[Kamiz, Obscura Oculus](https://scryfall.com/card/ncc/3/kamiz-obscura-oculus?utm_source=api) ({1}{W}{U}{B}):** Redundant Jin Sakai in the 99—grants unblockable + Connive to one attacker and Double Strike to another.
*   **[Drana, Liberator of Malakir](https://scryfall.com/card/lcc/193/drana-liberator-of-malakir?utm_source=api) ({1}{B}{B}):** 2/3 Flying First Strike; deals First Strike combat damage first and puts a +1/+1 counter on all attacking creatures before Regular Combat Damage resolves.
*   **[Nashi, Moon Sage's Scion](https://scryfall.com/card/otc/143/nashi-moon-sages-scion?utm_source=api) ({1}{B}{B}):** Exiles the top card of all 4 libraries on combat damage (twice with Double Strike) and casts them for life.
*   **[Grim Hireling](https://scryfall.com/card/clb/755/grim-hireling?utm_source=api) ({3}{B}):** Creates 2 Treasures per combat damage step per player—generating up to 12 Treasures in a single combat when three Double Strike attackers connect, while doubling as repeatable creature removal.
*   **[Rev, Tithe Extractor](https://scryfall.com/card/plst/J25-45/rev-tithe-extractor?utm_source=api) ({3}{B}):** Grants Deathtouch on attack (making First Strike lethal to any blocker) and creates a Treasure + steals a card per combat damage step per player.
*   **[Gonti, Night Minister](https://scryfall.com/card/dft/87/gonti-night-minister?utm_source=api) ({2}{B}{B}):** Turns every single creature's combat damage hit into a face-down card theft from that opponent's library (triggering twice per Double Strike creature).
*   **[Dragonlord Ojutai](https://scryfall.com/card/ncc/337/dragonlord-ojutai?utm_source=api) ({3}{W}{U}):** 5/4 Flyer with hexproof while untapped; with *Standoff* Double Strike, deals 10 flying damage and resolves two *Anticipate* triggers.
*   **[Yuriko, the Tiger's Shadow](https://scryfall.com/card/cmm/364/yuriko-the-tigers-shadow?utm_source=api) ({1}{U}{B}):** Premier Ninja draw and table-wide life drain engine; ideal for Ninjutsu-ing in after First Strike damage to deal Regular Combat Damage in the same combat.
*   **[Thousand-Faced Shadow](https://scryfall.com/card/neo/86/thousand-faced-shadow?utm_source=api) ({U}):** 1-mana flying attacker or Ninjutsu clone that creates an attacking token copy of your best Saboteur.
*   **[Mist-Syndicate Naga](https://scryfall.com/card/mh1/58/mist-syndicate-naga?utm_source=api) ({2}{U}):** Creates a permanent token copy of itself on combat damage—producing two permanent copies in one swing with *Standoff* Double Strike.
*   **[Fallen Shinobi](https://scryfall.com/card/otc/226/fallen-shinobi?utm_source=api) ({3}{U}{B}):** 5/4 Ninja that exiles the top 2 cards of the defending player's library and casts them for free (4 free cards with Double Strike).
*   **[Kaito, Bane of Nightmares](https://scryfall.com/card/dsk/220/kaito-bane-of-nightmares?utm_source=api) ({2}{U}{B}):** Ninjutsu Planeswalker that becomes a 3/4 Hexproof Ninja on your turn, creates permanent +1/+1 Ninja emblems, surveils/draws, and stuns blockers.
*   **[Spark Double](https://scryfall.com/card/rvr/62/spark-double?utm_source=api) ({3}{U}):** Enters as a non-legendary 3/5 copy of **Jin Sakai, Ghost of Tsushima**—allowing every solo attacker to receive **both Ghost (Unblockable) AND Standoff (Double Strike)** at the same time!

### ⚔️ Life-Halving Finishers & Combat Amplifiers (7 Cards)
*   **[Virtus the Veiled](https://scryfall.com/card/bbd/7/virtus-the-veiled?utm_source=api) ({2}{B}):** 1/1 Deathtouch Assassin that cuts the defending player's life in half on combat damage. With *Ghost* he is unblockable; with *Standoff* Double Strike he cuts 40 life $\rightarrow$ 20 $\rightarrow$ 10 in a single swing!
*   **[Quietus Spike](https://scryfall.com/card/ncc/377/quietus-spike?utm_source=api) ({3}):** Equipment granting Deathtouch and cutting the defending player's life in half on combat damage (triggers twice with Double Strike).
*   **[Vorpal Sword](https://scryfall.com/card/afr/124/vorpal-sword?utm_source=api) ({B}):** Cheap +2/+0 Deathtouch equipment whose `{5}{B}{B}{B}` activated ability turns any Jin Sakai *Ghost* (unblockable) attacker into an instant one-hit player elimination.
*   **[Duelist's Heritage](https://scryfall.com/card/tle/153/duelists-heritage?utm_source=api) ({2}{W}):** Grants Double Strike to an attacking creature every combat—allowing Jin Sakai to choose *Ghost* (Unblockable) on that creature so it gets both Unblockable and Double Strike.
*   **[Odric, Lunarch Marshal](https://scryfall.com/card/inr/36/odric-lunarch-marshal?utm_source=api) ({3}{W}):** Broadcasts Flying, Deathtouch, Lifelink, First Strike, Double Strike, and Indestructible across your entire team at the start of combat.
*   **[True Conviction](https://scryfall.com/card/c14/93/true-conviction?utm_source=api) ({3}{W}{W}{W}):** Grants your entire team permanent Double Strike and Lifelink, freeing Jin Sakai to choose *Ghost* (Unblockable) on all 3 solo attackers while they still hit twice.
*   **[Akroma's Will](https://scryfall.com/card/lcc/125/akromas-will?utm_source=api) ({3}{W}):** Game-ending instant finisher granting all creatures Flying, Vigilance, Double Strike, Lifelink, Indestructible, and Protection from all colors.

### 🛡️ Targeted Disruption & Commander Shielding (12 Cards — 0 Game Changers)
*   **[Swords to Plowshares](https://scryfall.com/card/msc/143/swords-to-plowshares?utm_source=api) ({W}):** 1-mana instant creature exile.
*   **[Path to Exile](https://scryfall.com/card/msc/141/path-to-exile?utm_source=api) ({W}):** 1-mana instant creature exile.
*   **[Mother of Runes](https://scryfall.com/card/clb/702/mother-of-runes?utm_source=api) ({W}):** Taps to give Jin Sakai protection from removal OR gives an attacker protection from a blocker's color so Jin Sakai can choose *Standoff* Double Strike.
*   **[Giver of Runes](https://scryfall.com/card/mh1/13/giver-of-runes?utm_source=api) ({W}):** Redundant Mother of Runes that also grants protection from colorless.
*   **[Pippin, Guard of the Citadel](https://scryfall.com/card/ltr/218/pippin-guard-of-the-citadel?utm_source=api) ({W}{U}):** 2/2 Vigilance Ward {1}; taps to grant protection from any card type—naming `creatures` makes an attacker 100% unblockable so Jin Sakai can give it *Standoff* Double Strike!
*   **[Counterspell](https://scryfall.com/search?q=!"Counterspell") ({U}{U}):** Unconditional 2-mana stack interaction.
*   **[Dovin's Veto](https://scryfall.com/search?q=!"Dovin's+Veto") ({W}{U}):** Uncounterable noncreature counterspell to stop opposing board wipes or combo wins.
*   **[Drown in the Loch](https://scryfall.com/search?q=!"Drown+in+the+Loch") ({U}{B}):** Versatile 2-mana modal counterspell or creature kill spell.
*   **[Despark](https://scryfall.com/card/tdc/284/despark?utm_source=api) ({W}{B}):** 2-mana instant exile for any threatening permanent with mana value $\ge 4$.
*   **[Anguished Unmaking](https://scryfall.com/search?q=!"Anguished+Unmaking") ({1}{W}{B}):** Instant-speed exile for any nonland permanent.
*   **[Void Rend](https://scryfall.com/card/snc/230/void-rend?utm_source=api) ({W}{U}{B}):** Uncounterable instant-speed nonland permanent removal.
*   **[Swiftfoot Boots](https://scryfall.com/card/mbc/77/swiftfoot-boots?utm_source=api) ({2}):** Grants Hexproof and Haste while still allowing you to target your own equipped creature with *Pippin*, *Mother of Runes*, and *Duelist's Heritage*.

### 💥 Mass Disruption & Asymmetric Sweepers (4 Cards)
*   **[Boromir, Warden of the Tower](https://scryfall.com/card/ltr/4/boromir-warden-of-the-tower?utm_source=api) ({2}{W}):** 3/3 Vigilance hatebear that counters opponents' free spells and sacrifices to make your entire board Indestructible through sweepers.
*   **[Toxic Deluge](https://scryfall.com/card/msc/161/toxic-deluge?utm_source=api) ({2}{B}):** 3-mana scalable sweeper that clears indestructible threats; at X=2 or X=3, Jin Sakai (2/4) often survives on the board!
*   **[Damn](https://scryfall.com/search?q=!"Damn") ({B}{B} / Overload {2}{W}{W}):** 2-mana spot removal early or 4-mana emergency board reset.
*   **[Time Wipe](https://scryfall.com/card/tdc/308/time-wipe?utm_source=api) ({2}{W}{W}{U}):** Returns **Jin Sakai** (or your best Saboteur) to hand before destroying all creatures on the battlefield.

### 🏔️ Lands (38 Cards — Pragmatic Low-Bracket-3 Mana Base, Zero Filter Lands)
*   **Rainbow & Tri-Color Fixing (5):** **[Command Tower](https://scryfall.com/search?q=!"Command+Tower")**, **[Exotic Orchard](https://scryfall.com/search?q=!"Exotic+Orchard")**, **[Raffine's Tower](https://scryfall.com/card/snc/254/raffines-tower?utm_source=api)**, **[Arcane Sanctum](https://scryfall.com/card/dsc/259/arcane-sanctum?utm_source=api)**, **[Path of Ancestry](https://scryfall.com/card/mbc/80/path-of-ancestry?utm_source=api)**.
*   **Untapped Pain Lands (3):** **[Adarkar Wastes](https://scryfall.com/card/eoc/147/adarkar-wastes?utm_source=api)**, **[Caves of Koilos](https://scryfall.com/card/soc/365/caves-of-koilos?utm_source=api)**, **[Underground River](https://scryfall.com/card/frc/87/underground-river?utm_source=api)**.
*   **Check Lands (3):** **[Glacial Fortress](https://scryfall.com/search?q=!"Glacial+Fortress")**, **[Isolated Chapel](https://scryfall.com/search?q=!"Isolated+Chapel")**, **[Drowned Catacomb](https://scryfall.com/search?q=!"Drowned+Catacomb")**.
*   **Slow Lands (3):** **[Deserted Beach](https://scryfall.com/search?q=!"Deserted+Beach")**, **[Shattered Sanctum](https://scryfall.com/card/sos/260/shattered-sanctum?utm_source=api)**, **[Shipwreck Marsh](https://scryfall.com/card/fra/189/shipwreck-marsh?utm_source=api)**.
*   **Modal Pathways (3):** **[Hengegate Pathway // Mistgate Pathway](https://scryfall.com/search?q=!"Hengegate+Pathway")**, **[Brightclimb Pathway // Grimclimb Pathway](https://scryfall.com/search?q=!"Brightclimb+Pathway")**, **[Clearwater Pathway // Murkwater Pathway](https://scryfall.com/search?q=!"Clearwater+Pathway")**.
*   **Battle / Tango Lands (2):** **[Prairie Stream](https://scryfall.com/card/msc/257/prairie-stream?utm_source=api)**, **[Sunken Hollow](https://scryfall.com/card/msc/271/sunken-hollow?utm_source=api)**.
*   **Reveal / Snarl Lands (3):** **[Choked Estuary](https://scryfall.com/card/msc/229/choked-estuary?utm_source=api)**, **[Port Town](https://scryfall.com/card/msc/256/port-town?utm_source=api)**, **[Shineshadow Snarl](https://scryfall.com/card/soc/403/shineshadow-snarl?utm_source=api)**.
*   **Tainted Lands (2):** **[Tainted Field](https://scryfall.com/card/dsc/302/tainted-field?utm_source=api)**, **[Tainted Isle](https://scryfall.com/card/dsc/303/tainted-isle?utm_source=api)**.
*   **Utility Lands (2):** **[Bojuka Bog](https://scryfall.com/search?q=!"Bojuka+Bog")** (graveyard exile), **[Reliquary Tower](https://scryfall.com/card/soc/398/reliquary-tower?utm_source=api)** (unlimited hand size for massive combat draw turns).
*   **Basic Lands (12):** **5 [Island](https://scryfall.com/search?q=!"Island")**, **4 [Swamp](https://scryfall.com/search?q=!"Swamp")**, **3 [Plains](https://scryfall.com/search?q=!"Plains")** (supports Check lands, Battle lands, Reveal lands, Tainted lands, and catch-up ramp).

---

## 🚀 Future Roadmap: Upgrades & Considerations

### 💡 High-Impact Tech to Consider (If Scaling to Mid/High Bracket 3 Later)
*   **[Brotherhood Regalia](https://scryfall.com/card/acr/71/brotherhood-regalia?utm_source=api) ({2}):** Grants Ward {2} and Unblockable (Equip Legendary {1}), letting Jin Sakai always select *Standoff* Double Strike on himself while staying protected.
*   **[Sword of Feast and Famine](https://scryfall.com/card/2xm/296/sword-of-feast-and-famine?utm_source=api) ({3}):** Untaps all your lands on First Strike AND Regular Combat Damage when equipped to a *Standoff* Double Strike attacker, doubling your mana every turn.
*   **[Teferi's Protection](https://scryfall.com/card/2x2/32/teferis-protection?utm_source=api) ({2}{W}) [GAME CHANGER]:** Optional Game Changer slot (`1 / 3`) if you decide to add premium phasing protection later.

### 🛒 Active Acquisition List (Priority Swaps)
| **New Card (In)** | **Card to Remove (Out)** | **Category** | **Status** |
| :--- | :--- | :--- | :--- |
| — | — | — | Baseline Established |

---

## 📜 Deck Changelog
*   **[2026-10-18]:** Initial Low Bracket 3 deck inception ("The Three-Front Standoff"), Goldfish validation (20 sims, 98% cast rate, 50% Gold Keeps, Turn 5.3 Engine Readiness), DTI calibration (33 / 96, 0/3 Game Changers, All Gates Passed), and MTG Forge synchronization.

---

## 🃏 Plain Text Copy/Paste (Moxfield Import)
COMMANDER:  
1 Jin Sakai, Ghost of Tsushima  

DECK:  
1 Adarkar Wastes  
1 Akroma's Will  
1 Anguished Unmaking  
1 Arcane Sanctum  
1 Arcane Signet  
1 Baleful Strix  
1 Bident of Thassa  
1 Bojuka Bog  
1 Boromir, Warden of the Tower  
1 Breena, the Demagogue  
1 Brightclimb Pathway // Grimclimb Pathway  
1 Caves of Koilos  
1 Cephalid Constable  
1 Choked Estuary  
1 Clearwater Pathway // Murkwater Pathway  
1 Command Tower  
1 Counterspell  
1 Damn  
1 Daxos of Meletis  
1 Deserted Beach  
1 Despark  
1 Dimir Cutpurse  
1 Dovin's Veto  
1 Dragonlord Ojutai  
1 Drana, Liberator of Malakir  
1 Drown in the Loch  
1 Drowned Catacomb  
1 Duelist's Heritage  
1 Enduring Curiosity  
1 Exotic Orchard  
1 Fallen Shinobi  
1 Fellwar Stone  
1 Giver of Runes  
1 Gix, Yawgmoth Praetor  
1 Glacial Fortress  
1 Gonti, Night Minister  
1 Grim Hireling  
1 Hengegate Pathway // Mistgate Pathway  
5 Island  
1 Isolated Chapel  
1 Kaito, Bane of Nightmares  
1 Kamiz, Obscura Oculus  
1 Lotho, Corrupt Shirriff  
1 Loyal Warhound  
1 Malcolm, Alluring Scoundrel  
1 Mist-Syndicate Naga  
1 Mother of Runes  
1 Nashi, Moon Sage's Scion  
1 Odric, Lunarch Marshal  
1 Ornithopter of Paradise  
1 Path of Ancestry  
1 Path to Exile  
1 Pippin, Guard of the Citadel  
3 Plains  
1 Port Town  
1 Prairie Stream  
1 Quietus Spike  
1 Raffine, Scheming Seer  
1 Raffine's Tower  
1 Reconnaissance Mission  
1 Reliquary Tower  
1 Rev, Tithe Extractor  
1 Satoru, the Infiltrator  
1 Shattered Sanctum  
1 Shineshadow Snarl  
1 Shipwreck Marsh  
1 Sol Ring  
1 Spark Double  
1 Sunken Hollow  
4 Swamp  
1 Swiftfoot Boots  
1 Sword of the Animist  
1 Swords to Plowshares  
1 Tainted Field  
1 Tainted Isle  
1 Talisman of Dominance  
1 Talisman of Hierarchy  
1 Talisman of Progress  
1 Thief of Sanity  
1 Thousand-Faced Shadow  
1 Time Wipe  
1 Toxic Deluge  
1 True Conviction  
1 Tymna the Weaver  
1 Underground River  
1 Virtus the Veiled  
1 Void Rend  
1 Vorpal Sword  
1 Wayfarer's Bauble  
1 Yuriko, the Tiger's Shadow  
