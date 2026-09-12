# MTG Board Wipes Reference Guide: The Top 20 Sweepers

> **Source:** Based on *"20 best board wipes in Magic: The Gathering"* by **Ryan Epps** ([Polygon](https://www.polygon.com/best-board-wipes-mtg-magic-gathering/)).  
> **Published:** September 8, 2026  
> **Purpose:** A centralized, tactical reference guide documenting the 20 premier mass removal spells in *Magic: The Gathering*, analyzing their mechanical vectors, asymmetry potential, bracket compliance, and ideal Commander archetypes.

---

## 🧭 1. Philosophy & Selection Criteria

In Commander, **Mass Disruption** (board wipes) is not merely defensive panic button insurance—it is a core tool of **tempo swinging, parity breaking, and game ending**. According to our project's `"New Era"` standard in [`COMMANDER_TEMPLATE.md`](COMMANDER_TEMPLATE.md), an average deck dedicates **~6 slots** to Mass Disruption.

Selecting the correct sweeper for a deck depends on **five tactical dimensions**:

1. **Mana Efficiency & Velocity:** Does the card break the baseline rate (traditionally 4 mana)? Sweepers like [**Toxic Deluge**](https://scryfall.com/search?q=!"Toxic+Deluge") ({2}{B}) or cost-reducers like [**Blasphemous Act**](https://scryfall.com/search?q=!"Blasphemous+Act") ({8}{R}) and [**Vanquish the Horde**](https://scryfall.com/search?q=!"Vanquish+the+Horde") allow you to wipe the board and develop a threat on the same turn.
2. **Timing & Speed:** Is it castable at instant speed? Wiping at instant speed (e.g., overloaded [**Cyclonic Rift**](https://scryfall.com/search?q=!"Cyclonic+Rift") on the opponent's end step) completely denies opponents untap steps while setting up an uncontested alpha strike.
3. **Removal Vector & Permanence:**
   - **Destroy:** Traditional (stops regeneration on older cards), but vulnerable to Indestructible (*Heroic Intervention*, *Teferi's Protection*).
   - **Exile:** Permanent removal ([**Farewell**](https://scryfall.com/search?q=!"Farewell"), [**Merciless Eviction**](https://scryfall.com/search?q=!"Merciless+Eviction")); bypasses indestructible, denies death triggers, and shuts down graveyard reanimation.
   - **Toughness Reduction (-X/-X):** State-based action ([**Toxic Deluge**](https://scryfall.com/search?q=!"Toxic+Deluge"), [**The Meathook Massacre**](https://scryfall.com/search?q=!"The+Meathook+Massacre")); bypasses indestructible, hexproof, and damage prevention.
   - **Library Tuck:** Bottom of library ([**Terminus**](https://scryfall.com/search?q=!"Terminus")); circumvents both graveyards and death triggers.
   - **Mass Bounce:** Nonland bounce ([**Cyclonic Rift**](https://scryfall.com/search?q=!"Cyclonic+Rift")); erases tokens forever and forces opponents to discard to hand size.
4. **Asymmetry & Parity Breaking:** Symmetrical wipes hurt the caster as much as opponents. Asymmetrical or modular wipes ([**Austere Command**](https://scryfall.com/search?q=!"Austere+Command"), [**Organic Extinction**](https://scryfall.com/search?q=!"Organic+Extinction"), [**Ezuri's Predation**](https://scryfall.com/search?q=!"Ezuri's+Predation"), [**In Garruk's Wake**](https://scryfall.com/search?q=!"In+Garruk's+Wake")) spare your own board, turning a wipe directly into a win.
5. **Bracket System Compliance:**
   - As codified in [`COMMANDER_DECKBUILDING_RULES.md`](COMMANDER_DECKBUILDING_RULES.md), **Game Changers** are strictly restricted:
     - **Brackets 1–2:** **0** Game Changers allowed.
     - **Bracket 3:** Up to **3** Game Changers allowed.
     - **Brackets 4–5:** Unrestricted.
   - On this list, [**Cyclonic Rift**](https://scryfall.com/search?q=!"Cyclonic+Rift") and [**Farewell**](https://scryfall.com/search?q=!"Farewell") are official **Game Changers**. The remaining 18 sweepers are regular format-legal cards that consume 0 Game Changer slots.

---

## 📊 2. Quick Reference Matrix

| Rank | Card | Mana Cost | Color / Identity | Type & Speed | Removal Vector | Scope / Parity | Game Changer? |
|:---:|---|---|:---:|---|---|---|:---:|
| **#1** | [**Cyclonic Rift**](https://scryfall.com/search?q=!"Cyclonic+Rift") | {1}{U} / {6}{U} | 🔵 Blue | Instant | Bounce to hand | Asymmetrical (Opponents only) | ⚠️ **YES** |
| **#2** | [**Farewell**](https://scryfall.com/search?q=!"Farewell") | {4}{W}{W} | ⚪ White | Sorcery | Non-targeting Exile | Symmetrical / Modular (Choose 1+) | ⚠️ **YES** |
| **#3** | [**Toxic Deluge**](https://scryfall.com/search?q=!"Toxic+Deluge") | {2}{B} | ⚫ Black | Sorcery | Stats reduction (-X/-X) | Scalable / Life-paid | No |
| **#4** | [**Damnation**](https://scryfall.com/search?q=!"Damnation") | {2}{B}{B} | ⚫ Black | Sorcery | Destroy (No regen) | Symmetrical | No |
| **#5** | [**Wrath of God**](https://scryfall.com/search?q=!"Wrath+of+God") | {2}{W}{W} | ⚪ White | Sorcery | Destroy (No regen) | Symmetrical | No |
| **#6** | [**Supreme Verdict**](https://scryfall.com/search?q=!"Supreme+Verdict") | {1}{W}{W}{U} | ⚪🔵 Azorius | Sorcery (Uncounterable) | Destroy | Symmetrical | No |
| **#7** | [**Blasphemous Act**](https://scryfall.com/search?q=!"Blasphemous+Act") | {8}{R} ({R} min) | 🔴 Red | Sorcery | 13 Damage | Symmetrical / Cost Reduction | No |
| **#8** | [**Terminus**](https://scryfall.com/search?q=!"Terminus") | {4}{W}{W} / {W} | ⚪ White | Sorcery (Miracle) | Tuck (Bottom of library) | Symmetrical / Miracle velocity | No |
| **#9** | [**The Meathook Massacre**](https://scryfall.com/search?q=!"The+Meathook+Massacre") | {X}{B}{B} | ⚫ Black | Leg. Enchantment | Stats reduction (-X/-X) | Persistent Drain Engine | No |
| **#10** | [**Fumigate**](https://scryfall.com/search?q=!"Fumigate") | {3}{W}{W} | ⚪ White | Sorcery | Destroy + Life buffer | Symmetrical + Lifegain | No |
| **#11** | [**Austere Command**](https://scryfall.com/search?q=!"Austere+Command") | {4}{W}{W} | ⚪ White | Sorcery | Destroy | Modular (Choose 2 of 4) | No |
| **#12** | [**Earthquake**](https://scryfall.com/search?q=!"Earthquake") | {X}{R} | 🔴 Red | Sorcery | X Ground Damage + Burn | Asymmetrical (Non-fliers) | No |
| **#13** | [**Living Death**](https://scryfall.com/search?q=!"Living+Death") | {3}{B}{B} | ⚫ Black | Sorcery | Mass Sacrifice + Mass Reanimate | Parity Inversion (Graveyard swap) | No |
| **#14** | [**Merciless Eviction**](https://scryfall.com/search?q=!"Merciless+Eviction") | {4}{W}{B} | ⚪⚫ Orzhov | Sorcery | Total Exile | Modal (Choose 1 permanent type) | No |
| **#15** | [**Armageddon**](https://scryfall.com/search?q=!"Armageddon") | {3}{W} | ⚪ White | Sorcery | Destroy Lands (MLD) | Total Land Wipe | No |
| **#16** | [**Nevinyrral's Disk**](https://scryfall.com/search?q=!"Nevinyrral's+Disk") | {4} | 🟤 Colorless | Artifact ({1}, {T}) | Destroy | Rattlesnake On-Board Threat | No |
| **#17** | [**Ezuri's Predation**](https://scryfall.com/search?q=!"Ezuri's+Predation") | {5}{G}{G}{G} | 🟢 Green | Sorcery | 4/4 Fight Triggers | Asymmetrical (Opponents only) | No |
| **#18** | [**In Garruk's Wake**](https://scryfall.com/search?q=!"In+Garruk's+Wake") | {7}{B}{B} | ⚫ Black | Sorcery | Destroy Creatures & Walkers | Asymmetrical (Opponents only) | No |
| **#19** | [**Organic Extinction**](https://scryfall.com/search?q=!"Organic+Extinction") | {8}{W}{W} | ⚪ White | Sorcery (Improvise) | Destroy Non-Artifacts | Asymmetrical (Artifact shells) | No |
| **#20** | [**Boompile**](https://scryfall.com/search?q=!"Boompile") | {4} | 🟤 Colorless | Artifact ({T} + Coin Flip) | Destroy Nonlands | Universal Colorless Emergency | No |

---

## 🔍 3. Deep-Dive Card Analysis (Ranked #1 to #20)

### #1. [Cyclonic Rift](https://scryfall.com/search?q=!"Cyclonic+Rift")
- **Mana Cost:** {1}{U} (Single Target) / Overload {6}{U} (All Opponents)
- **Type:** Instant
- **Oracle Text:** *Return target nonland permanent you don't control to its owner's hand. Overload {6}{U} (You may cast this spell for its overload cost. If you do, change "target" in its text to "each.")*
- **Bracket Status:** ⚠️ **Game Changer** (Max 3 in Bracket 3; strictly 0 in Brackets 1–2).
- **Author's Take:** Widely feared as the single most powerful blue spell in multiplayer Magic. Playing it at instant speed for 7 mana clears all opposing boards, wipes away every token permanently, and forces opponents to waste subsequent turns recasting cards while your own board remains fully intact.
- **Why It's Premier:**
  - **Instant Speed:** Can be cast on the end step right before your turn, leaving opponents tapped out with empty boards while you untap with a full army.
  - **Total Nonland Scope:** Bounces planeswalkers, enchantments, artifacts, and creatures alike.
  - **Token Annihilation:** Token creatures and copies cease to exist upon leaving the battlefield, causing permanent card disadvantage to go-wide swarm decks.
- **Ideal Decks:** High-power control, Spellslinger, and any blue deck operating in Bracket 3–5.

---

### #2. [Farewell](https://scryfall.com/search?q=!"Farewell")
- **Mana Cost:** {4}{W}{W}
- **Type:** Sorcery
- **Oracle Text:** *Choose one or more — Exile all artifacts. Exile all creatures. Exile all enchantments. Exile all graveyards.*
- **Bracket Status:** ⚠️ **Game Changer** (Max 3 in Bracket 3; strictly 0 in Brackets 1–2).
- **Author's Take:** Redefined white board wipes upon release in *Kamigawa: Neon Dynasty*. Offering modular flexibility alongside total non-targeting exile, it systematically dismantles multiple permanent types while simultaneously nuking graveyards to deny recursive lines.
- **Why It's Premier:**
  - **Modular Exile:** You pick only the modes you want. If you are playing an Enchantress deck, exile artifacts, creatures, and graveyards while preserving your enchantments.
  - **Complete Bypass:** Sidesteps indestructible (*Avacyn*, *Heroic Intervention*), ignores regeneration, stops on-death triggers (*Blood Artist*, *Zulaport Cutthroat*), and denies recursion.
  - **Nuclear Reset:** Resolving Farewell effectively ends infinite graveyard loops, Treasure hoard piles, and Superfriends token swarms in one stroke.
- **Ideal Decks:** White Control, Superfriends ([*Atraxa, Praetors' Voice*](commander_decks/Planning/AtraxaPraetorsVoice/atraxa_superfriends.md)), Enchantress, or Anti-Graveyard midrange.

---

### #3. [Toxic Deluge](https://scryfall.com/search?q=!"Toxic+Deluge")
- **Mana Cost:** {2}{B}
- **Type:** Sorcery
- **Oracle Text:** *As an additional cost to cast this spell, pay X life. All creatures get -X/-X until end of turn.*
- **Bracket Status:** Regular (0 Game Changer slots consumed).
- **Author's Take:** The single most efficient board wipe in *Magic*'s history. At just 3 mana, it breaks the standard 4-mana sweeper curve by converting life points into mass stat reduction.
- **Why It's Premier:**
  - **3-Mana Curve Breaker:** Leaves mana open to deploy your own follow-up threats or hold up countermagic/protection.
  - **State-Based -X/-X:** Bypasses Indestructible, Hexproof, Shroud, Ward, and damage-prevention shields.
  - **Surgical Scale:** You pay only the exact life needed. To wipe an opponent's army of 2/2 tokens and utility dorks while keeping your 6/6 commander alive, simply pay 3 life.
- **Ideal Decks:** Black Midrange, Control, Aristocrats, Lifegain shells, cEDH / Bracket 3–4 decks ([*Atraxa*](commander_decks/Planning/AtraxaPraetorsVoice/atraxa_superfriends.md), [*Sauron*](commander_decks/Owned/SauronTheDarkLord/README.md), [*Meren*](commander_decks/Owned/Meren/README.md)).

---

### #4. [Damnation](https://scryfall.com/search?q=!"Damnation")
- **Mana Cost:** {2}{B}{B}
- **Type:** Sorcery
- **Oracle Text:** *Destroy all creatures. They can't be regenerated.*
- **Bracket Status:** Regular.
- **Author's Take:** Originally printed in *Planar Chaos* as a color-shifted mirror of *Wrath of God*, Damnation gave mono-black and black-heavy decks unconditional mass creature removal without needing to splash white.
- **Why It's Premier:**
  - **Baseline 4-Mana Efficiency:** Flawless clean destruction at the fundamental curve rate.
  - **Regeneration Denial:** Shuts down classic green/black regeneration tricks.
  - **Graveyard Synergies:** Unlike exile, sending creatures to the graveyard fuels your own *Reanimate*, *Living Death*, and death-trigger engines.
- **Ideal Decks:** Mono-Black Control, Golgari/Dimir/Mardu midrange, Reanimator.

---

### #5. [Wrath of God](https://scryfall.com/search?q=!"Wrath+of+God")
- **Mana Cost:** {2}{W}{W}
- **Type:** Sorcery
- **Oracle Text:** *Destroy all creatures. They can't be regenerated.*
- **Bracket Status:** Regular.
- **Author's Take:** The 1993 *Alpha* original and the foundational baseline against which all creature sweepers have been measured for over three decades. Simple, elegant, and uncompromising.
- **Why It's Premier:**
  - **The 4-Mana Standard:** Zero gimmicks, zero setup requirements.
  - **Reliable Budget Pricing:** Extensive reprints keep it accessible (~$3–$4).
  - **Stops Regeneration:** Ensures older threats stay dead.
- **Ideal Decks:** White Weenie insurance, Azorius/Esper Control, Angel Tribal ([*Karametra*](commander_decks/Owned/KarametraAngels/README.md)).

---

### #6. [Supreme Verdict](https://scryfall.com/search?q=!"Supreme+Verdict")
- **Mana Cost:** {1}{W}{W}{U}
- **Type:** Sorcery
- **Oracle Text:** *This spell can't be countered. Destroy all creatures.*
- **Bracket Status:** Regular.
- **Author's Take:** Return to Ravnica's gift to control players. The "can't be countered" clause eliminates the nightmare scenario of spending 4 mana to clear an overwhelming board only to be stopped by a 2-mana *Counterspell* or *Fierce Guardianship*.
- **Why It's Premier:**
  - **Uncounterable Insurance:** Guaranteed resolution through blue counter suites and Ward/tax effects.
  - **Tempo Reversal:** Completely blows out tempo and aggro-control players who overextended believing their counterspells would protect them.
- **Ideal Decks:** Azorius ({W}{U}), Esper ({W}{U}{B}), Jeskai ({U}{R}{W}), and Bant ({G}{W}{U}) control decks.

---

### #7. [Blasphemous Act](https://scryfall.com/search?q=!"Blasphemous+Act")
- **Mana Cost:** {8}{R} (Reduces to {R} minimum)
- **Type:** Sorcery
- **Oracle Text:** *This spell costs {1} less to cast for each creature on the battlefield. Blasphemous Act deals 13 damage to each creature.*
- **Bracket Status:** Regular.
- **Author's Take:** Red's undisputed king of mass removal. In a 4-player Commander game, having 8+ total creatures on board is effortless, consistently reducing this spell's cost to a single {R} mana.
- **Why It's Premier:**
  - **1-Mana Sweeper:** Spending 1 mana to clear the table leaves 4–6+ mana open to rebuild your own board on the same turn.
  - **13 Damage Annihilation:** Lethal for virtually every commander and massive threat in the format.
  - **Burn Synergy:** Synergizes with damage-reflecting creatures like *Brash Taunter*, *Stuffy Doll*, or *Wrathful Red Dragon* to convert a board wipe into lethal burn aimed directly at opponents' life totals.
- **Ideal Decks:** Any deck with Red identity ([*Henzie*](commander_decks/Planning/HenzieBlitz/henzie_blitz.md), [*Caesar*](commander_decks/Planning/CaesarLegionsEmperor/caesar_mardu.md), [*The Ur-Dragon*](commander_decks/Owned/UrDragon/README.md), [*Sauron*](commander_decks/Owned/SauronTheDarkLord/README.md)).

---

### #8. [Terminus](https://scryfall.com/search?q=!"Terminus")
- **Mana Cost:** {4}{W}{W} / Miracle {W}
- **Type:** Sorcery
- **Oracle Text:** *Put all creatures on the bottom of their owners' libraries. Miracle {W} (You may cast this card for its miracle cost when you draw it if it's the first card you drew this turn.)*
- **Bracket Status:** Regular.
- **Author's Take:** Showcasing the *Miracle* mechanic from *Avacyn Restored*, Terminus lets you wipe the entire creature board for a single white mana if drawn as your first card. Tuck-to-bottom completely circumvents indestructible and graveyard reanimation.
- **Why It's Premier:**
  - **1-Mana Instant-Speed Potential:** If triggered on an opponent's turn via instant-speed draw (*Brainstorm*, *Opt*, *Sensei's Divining Top*), it acts as a 1-mana instant-speed sweeper.
  - **Library Tuck:** Commanders tucked to the bottom can be redirected to the Command Zone, but regular threats cannot be reanimated, regenerated, or saved via indestructible shields.
- **Ideal Decks:** Topdeck manipulation decks (*Aminatou*, *Yennett*, *Elsha*), Miracles control shells.

---

### #9. [The Meathook Massacre](https://scryfall.com/search?q=!"The+Meathook+Massacre")
- **Mana Cost:** {X}{B}{B}
- **Type:** Legendary Enchantment
- **Oracle Text:** *When The Meathook Massacre enters, each creature gets -X/-X until end of turn. Whenever a creature you control dies, each opponent loses 1 life. Whenever a creature an opponent controls dies, you gain 1 life.*
- **Bracket Status:** Regular.
- **Author's Take:** A dual-purpose weapon that combines scalable -X/-X removal with a permanent aristocrat drain engine. It dominated Standard to the point of being banned, and remains a multi-format powerhouse.
- **Why It's Premier:**
  - **Permanent Presence:** Unlike sorceries that leave the stack, Meathook stays on the battlefield to provide ongoing life drain whenever any creature dies on either side.
  - **Immediate Stabilization:** Wiping 8 creatures immediately drains opponents and pads your life total, creating an insurmountable swing against aggro.
  - **Win Condition in Aristocrats:** Directly converts wide token sacs into game-ending life drain.
- **Ideal Decks:** Aristocrats ([*Caesar, Legion's Emperor*](commander_decks/Planning/CaesarLegionsEmperor/caesar_mardu.md), [*Mahadi*](commander_decks/Planning/MahadiEmporiumMaster/README.md)), Black Token engines, Lifegain/Drain decks.

---

### #10. [Fumigate](https://scryfall.com/search?q=!"Fumigate")
- **Mana Cost:** {3}{W}{W}
- **Type:** Sorcery
- **Oracle Text:** *Destroy all creatures. You gain 1 life for each creature destroyed this way.*
- **Bracket Status:** Regular (~$0.25 budget staple).
- **Author's Take:** Solves the primary weakness of control decks: falling to low life totals before landing a sweeper. By gaining 1 life per creature destroyed, clearing a wide token board can net 10–20+ life, completely resetting the clock.
- **Why It's Premier:**
  - **Immediate Defensive Buffer:** Puts you safely out of burn and haste range.
  - **Budget Staple:** Dirt cheap acquisition cost under $0.50.
- **Ideal Decks:** Lifegain synergies (*Lathiel*, *Karlov of the Ghost Council*, *Trostani*), Budget White control builds.

---

### #11. [Austere Command](https://scryfall.com/search?q=!"Austere+Command")
- **Mana Cost:** {4}{W}{W}
- **Type:** Sorcery
- **Oracle Text:** *Choose two — Destroy all artifacts; or Destroy all enchantments; or Destroy all creatures with mana value 3 or less; or Destroy all creatures with mana value 4 or greater.*
- **Bracket Status:** Regular.
- **Author's Take:** The pinnacle of tactical flexibility since *Lorwyn*. Choosing two distinct modes out of four allows you to tailor the wipe precisely to favor your own board state.
- **Why It's Premier:**
  - **Surgical Parity Breaking:**
    - High-CMC Big Stompy decks can destroy all CMC <= 3 creatures + enchantments, keeping their 6/6 Dragons and Angels intact.
    - Low-CMC Token/Weenie decks can destroy all CMC >= 4 creatures + artifacts, preserving their token swarms while destroying opposing bombs.
  - **Noncreature Utility:** Cleans up problematic artifact and enchantment engines without needing separate Disenchant slots.
- **Ideal Decks:** Midrange decks, Dragon/Angel tribal ([*Kibler's Flight / Ur-Dragon*](commander_decks/Owned/UrDragon/README.md), [*Karametra*](commander_decks/Owned/KarametraAngels/README.md)), Modular control.

---

### #12. [Earthquake](https://scryfall.com/search?q=!"Earthquake")
- **Mana Cost:** {X}{R}
- **Type:** Sorcery
- **Oracle Text:** *Earthquake deals X damage to each creature without flying and each player.*
- **Bracket Status:** Regular (~$0.50 budget).
- **Author's Take:** An *Alpha* foundational sweeper that scales from Turn 2 mana-dork clearing up to late-game player burn. Because it only damages non-flying creatures, airborne decks use it to scorch the earth while leaving their aerial armada untouched.
- **Why It's Premier:**
  - **Asymmetric Flying Parity:** Decks built around Dragons, Angels, Demons, or Thopters suffer zero damage to their creatures.
  - **Dual-Purpose Finisher:** Wipes the opposing ground defense while burning every player, closing out games when opponents are at low life.
- **Ideal Decks:** Flying Typal shells ([*The Ur-Dragon*](commander_decks/Owned/UrDragon/README.md), *Kaalia of the Vast*, *Kykar*), Big-Mana Red engines.

---

### #13. [Living Death](https://scryfall.com/search?q=!"Living+Death")
- **Mana Cost:** {3}{B}{B}
- **Type:** Sorcery
- **Oracle Text:** *Each player exiles all creature cards from their graveyard, then sacrifices all creatures they control, then puts all cards they exiled this way onto the battlefield.*
- **Bracket Status:** Regular.
- **Author's Take:** Equal parts mass removal and lethal game-ender. A *Tempest* staple that forces every player to sacrifice their battlefield and swap it with all creatures in their graveyard.
- **Why It's Premier:**
  - **Mass Sacrifice Bypass:** Sacrificing bypasses indestructible, protection, and ward.
  - **Parity Inversion:** When played in a self-mill, dredge, or discard shell, you wipe opponents' meager boards while reanimating 10–20 massive threats and ETB triggers onto your side.
  - **One-Card Win Con:** Often ends the game on resolution through hasty reanimated armies or ETB drain triggers (*Gary*, *Terror of the Peaks*, *Syr Konrad*).
- **Ideal Decks:** Reanimator & Graveyard value ([*Meren of Clan Nel Toth*](commander_decks/Owned/Meren/README.md), [*Henzie "Toolbox" Torre*](commander_decks/Planning/HenzieBlitz/henzie_blitz.md), [*The Necrobloom*](commander_decks/Planning/TheNecrobloom/necrobloom_abzan.md)).

---

### #14. [Merciless Eviction](https://scryfall.com/search?q=!"Merciless+Eviction")
- **Mana Cost:** {4}{W}{B}
- **Type:** Sorcery
- **Oracle Text:** *Choose one — Exile all artifacts; or Exile all creatures; or Exile all enchantments; or Exile all planeswalkers.*
- **Bracket Status:** Regular.
- **Author's Take:** The Orzhov hallmark of total non-targeting exile. It forces a choice of one permanent type and permanently eliminates every instance of it across the board.
- **Why It's Premier:**
  - **Permanent Neutralization:** Nullifies death triggers, indestructible, and recursion lines.
  - **Planeswalker Sweeper:** One of the rare board wipes capable of cleanly exiling an entire Superfriends board without hurting creature armies.
  - **Enchantment / Artifact Hose:** Completely eradicates Urza artifact piles or Pillowfort enchantment mazes.
- **Ideal Decks:** Orzhov ({W}{B}), Mardu ({R}{W}{B}), Esper ({W}{U}{B}), and Abzan ({W}{B}{G}) control shells.

---

### #15. [Armageddon](https://scryfall.com/search?q=!"Armageddon")
- **Mana Cost:** {3}{W}
- **Type:** Sorcery
- **Oracle Text:** *Destroy all lands.*
- **Bracket Status:** Regular (though heavily regulated by Rule 0 in casual pods).
- **Author's Take:** The most infamous land wipe in *Magic* history. While mass land destruction (MLD) is heavily taboo in casual Commander, in optimized and competitive pods it serves as a ruthless win-condition lock when you already hold superior board presence.
- **Why It's Premier:**
  - **Game Lockout:** If you control a dominant board (or indestructible lands via *Heroic Intervention* or *Avacyn*), wiping all lands prevents opponents from ever answering your threats.
  - **Parity Breaking:** Breaks parity with mana rocks (*Sol Ring*, *Mana Crypt*, *Moxes*), mana dorks, or land reanimation commanders (*Thalia and The Gitrog Monster*, *Lord Windgrace*).
- **Ideal Decks:** Stax, Hatebears, Competitive White/Abzan shells, Parity-breaking Landfall.

---

### #16. [Nevinyrral's Disk](https://scryfall.com/search?q=!"Nevinyrral's+Disk")
- **Mana Cost:** {4} (Activation: {1}, {T})
- **Type:** Artifact
- **Oracle Text:** *This artifact enters tapped. {1}, {T}: Destroy all artifacts, creatures, and enchantments.*
- **Bracket Status:** Regular.
- **Author's Take:** *Alpha*'s original colorless panic button (an homage to sci-fi author Larry Niven). Because it costs only generic mana, any deck regardless of color identity can run it to wipe artifacts, creatures, and enchantments simultaneously.
- **Why It's Premier:**
  - **Universal Colorless Access:** Crucial for colors lacking creature or enchantment wipes (Mono-Red, Mono-Blue, Mono-Black, Colorless Eldrazi).
  - **Rattlesnake Deterrence:** Sitting openly on the table forces opponents to second-guess playing additional threats.
  - **Untap Combos:** Combining with *Unwinding Clock*, *Clock of Omens*, or *Voltaic Key* lets you untap and detonate immediately.
- **Ideal Decks:** Colorless/Eldrazi ([*Ulamog Ramp*](commander_decks/Planning/UlamogRamp/README.md), [*Ulalek*](commander_decks/Planning/UlalekFusedAtrocity/README.md)), Mono-Blue, Artifact control shells.

---

### #17. [Ezuri's Predation](https://scryfall.com/search?q=!"Ezuri's+Predation")
- **Mana Cost:** {5}{G}{G}{G}
- **Type:** Sorcery
- **Oracle Text:** *For each creature your opponents control, create a 4/4 green Phyrexian Beast creature token. Each of those tokens fights a different one of those creatures.*
- **Bracket Status:** Regular.
- **Author's Take:** Green is notoriously deprived of traditional creature board wipes. Ezuri's Predation solves this by creating a 4/4 Phyrexian Beast for each enemy creature and forcing them to fight, simultaneously wiping out enemy utility creatures and leaving behind a massive army.
- **Why It's Premier:**
  - **Pure Green Creature Sweeper:** Provides mono-green and green-heavy decks with mass creature interaction without needing black or white.
  - **Overwhelming Board Presence:** Crushes token swarms (1/1s, 2/2s, 3/3s) with 0 losses to your Beasts, leaving you with an army of 4/4s ready to swing for lethal on the next turn.
  - **ETB Trigger Bonanza:** Triggers Landfall, creature-ETB card draw (*Tribute to the World Tree*, *Garruk's Packleader*), and token doublers (*Doubling Season*).
- **Ideal Decks:** Mono-Green Stompy, Big-Mana Ramp ([*The Necrobloom*](commander_decks/Planning/TheNecrobloom/necrobloom_abzan.md), [*Karametra*](commander_decks/Owned/KarametraAngels/README.md), [*Bruce Banner / Hulk*](commander_decks/Owned/IncredibleHulk/README.md)).

---

### #18. [In Garruk's Wake](https://scryfall.com/search?q=!"In+Garruk's+Wake")
- **Mana Cost:** {7}{B}{B}
- **Type:** Sorcery
- **Oracle Text:** *Destroy all creatures you don't control and all planeswalkers you don't control.*
- **Bracket Status:** Regular.
- **Author's Take:** When pure one-sided annihilation is worth the steep 9-mana cost. Wipes all opposing creatures and planeswalkers while leaving your entire board untouched.
- **Why It's Premier:**
  - **Zero Downside Asymmetry:** Unlike symmetrical wipes where you lose your own attackers and defenses, your creatures remain on the board ready for an immediate alpha strike.
  - **Hits Planeswalkers:** Completely erases opposing Superfriends loyalty engines.
  - **Easy in Black Big-Mana:** Mono-black ramp tools (*Cabal Coffers*, *Crypt Ghast*, *Bolas's Citadel*) easily generate 9 mana by Turn 6–7.
- **Ideal Decks:** Mono-Black Control, Big-Mana Black, Reanimation/Cost-cheating shells.

---

### #19. [Organic Extinction](https://scryfall.com/search?q=!"Organic+Extinction")
- **Mana Cost:** {8}{W}{W} (Improvise)
- **Type:** Sorcery
- **Oracle Text:** *Improvise (Your artifacts can help cast this spell. Each artifact you tap after you're done activating mana abilities pays for {1}.) Destroy all nonartifact creatures.*
- **Bracket Status:** Regular (~$0.30 budget).
- **Author's Take:** The ultimate asymmetric tool for artifact-based decks from *Kamigawa: Neon Dynasty Commander*. While 10 mana appears expensive, tapping artifacts (Equipment, Clues, Foods, Treasures, Thopters) frequently reduces the casting cost to just {W}{W}.
- **Why It's Premier:**
  - **One-Sided Meatgrinder:** Destroys all opposing flesh-and-blood armies while leaving your artifact creatures, Thopters, Constructs, and commanders completely untouched.
  - **Turns Defense into an Alpha Strike:** Tap your utility artifacts to cast it, clear out every blocker, and swing with your unaffected mechanized army.
- **Ideal Decks:** Artifact decks, Voltron/Equipment shells ([*Captain America*](commander_decks/Owned/CaptainAmerica/README.md)), Thopter/Construct swarm decks.

---

### #20. [Boompile](https://scryfall.com/search?q=!"Boompile")
- **Mana Cost:** {4} (Activation: {T})
- **Type:** Artifact
- **Oracle Text:** *{T}: Flip a coin. If you win the flip, destroy all nonland permanents.*
- **Bracket Status:** Regular.
- **Author's Take:** A high-stakes, unpredictable colorless reset button. For 4 generic mana, you can tap it the turn it enters; if you win the coin flip, it instantly detonates all nonland permanents, giving opponents zero warning.
- **Why It's Premier:**
  - **Immediate Activation:** Unlike *Nevinyrral's Disk*, Boompile does **not** enter the battlefield tapped.
  - **Nonland Scope:** Destroys planeswalkers, enchantments, artifacts, and creatures alike.
  - **Coin Flip Synergies:** Decks running *Krark's Thumb* get two chances to win the flip (75% success rate).
- **Ideal Decks:** Coin-flip chaos decks (*Okaun // Zndrsplt*, *Yusri*), Colorless Eldrazi builds, Budget emergency buttons.

---

## 🏆 4. Strategic Archetype Matrix: Which Wipe for Which Deck?

To help align deck construction with our project's existing decks, use this cross-reference guide:

| Commander / Archetype | Optimal Board Wipes to Prioritize | Rationale |
|---|---|---|
| **Dragons / Angels / Flyers**<br>([*The Ur-Dragon*](commander_decks/Owned/UrDragon/README.md), [*Karametra*](commander_decks/Owned/KarametraAngels/README.md)) | [**Earthquake**](https://scryfall.com/search?q=!"Earthquake"), [**Austere Command**](https://scryfall.com/search?q=!"Austere+Command"), [**Blasphemous Act**](https://scryfall.com/search?q=!"Blasphemous+Act") | *Earthquake* misses all flyers; *Austere Command* preserves high-CMC bombs while clearing low-mana swarms and enchantments. |
| **Artifacts & Equipment Voltron**<br>([*Captain America*](commander_decks/Owned/CaptainAmerica/README.md)) | [**Organic Extinction**](https://scryfall.com/search?q=!"Organic+Extinction"), [**Austere Command**](https://scryfall.com/search?q=!"Austere+Command"), [**Vanquish the Horde**](https://scryfall.com/search?q=!"Vanquish+the+Horde") | *Organic Extinction* uses Equipment to pay for mana and spares artifact creatures; avoid non-selective artifact wipes like *Farewell*! |
| **Aristocrats & Tokens**<br>([*Caesar*](commander_decks/Planning/CaesarLegionsEmperor/caesar_mardu.md), [*Mahadi*](commander_decks/Planning/MahadiEmporiumMaster/README.md)) | [**The Meathook Massacre**](https://scryfall.com/search?q=!"The+Meathook+Massacre"), [**Toxic Deluge**](https://scryfall.com/search?q=!"Toxic+Deluge"), [**Blasphemous Act**](https://scryfall.com/search?q=!"Blasphemous+Act") | *Meathook* directly drains opponents when tokens die; *Blasphemous Act* drops to 1 red mana with wide boards. |
| **Graveyard & Reanimator**<br>([*Meren*](commander_decks/Owned/Meren/README.md), [*Henzie Blitz*](commander_decks/Planning/HenzieBlitz/henzie_blitz.md)) | [**Living Death**](https://scryfall.com/search?q=!"Living+Death"), [**Damnation**](https://scryfall.com/search?q=!"Damnation"), [**Toxic Deluge**](https://scryfall.com/search?q=!"Toxic+Deluge") | *Living Death* is an asymmetric win-con that swaps graveyards with boards. **Avoid** running *Farewell* or *Merciless Eviction* in your own graveyard decks! |
| **Superfriends / Planeswalkers**<br>([*Atraxa Superfriends*](commander_decks/Planning/AtraxaPraetorsVoice/atraxa_superfriends.md)) | [**Farewell**](https://scryfall.com/search?q=!"Farewell"), [**Supreme Verdict**](https://scryfall.com/search?q=!"Supreme+Verdict"), [**Toxic Deluge**](https://scryfall.com/search?q=!"Toxic+Deluge") | Neither *Farewell* nor *Supreme Verdict* touches planeswalkers, clearing opposing creatures while leaving your planeswalker fortress untouched. |
| **Big Mana Green / Lands Matter**<br>([*The Necrobloom*](commander_decks/Planning/TheNecrobloom/necrobloom_abzan.md), [*Bruce Banner / Hulk*](commander_decks/Owned/IncredibleHulk/README.md)) | [**Ezuri's Predation**](https://scryfall.com/search?q=!"Ezuri's+Predation"), [**Toxic Deluge**](https://scryfall.com/search?q=!"Toxic+Deluge") | *Ezuri's Predation* turns massive mana ramp into an overwhelming token army while devouring opponents' boards. |

---

## 💡 5. Honorable Mentions & Key Variants

The article and community discussions highlight several critical variants worth tracking:

1. [**Vanquish the Horde**](https://scryfall.com/search?q=!"Vanquish+the+Horde") ({6}{W}{W}): The white sister spell to *Blasphemous Act*. Reduces its cost by {1} for each creature on the battlefield down to {W}{W}, providing an unconditional 2-mana board wipe in multiplayer pods.
2. [**Sublime Exhalation**](https://scryfall.com/search?q=!"Sublime+Exhalation") ({6}{W}): Features *Undaunted*, consistently costing {3}{W} (4 mana) in 4-player Commander games.
3. [**Scourglass**](https://scryfall.com/search?q=!"Scourglass") ({3}{W}{W}): An artifact-based board wipe that specifically spares artifacts and lands during upkeep, acting as a one-sided wipe in heavy artifact shells.
4. [**Ravages of War**](https://scryfall.com/search?q=!"Ravages+of+War") ({3}{W}): The *Portal Three Kingdoms* functional reprint of *Armageddon*, offering redundant mass land destruction for high-powered lockouts.
5. [**Damn**](https://scryfall.com/search?q=!"Damn") ({B}{B} / Overload {2}{W}{W}): Highly requested in article comments; functions as targeted spot removal for {B}{B} or an unconditional *Wrath of God* for {2}{W}{W}, offering supreme modal flexibility in Orzhov+ decks.
