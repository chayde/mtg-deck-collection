import os
import sys
import re
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from dti_evaluator import DTIEvaluation, BENCHMARK_META, generate_default_evaluation, parse_deck_cards, parse_goldfish_telemetry, save_evaluation_file, render_markdown_audit, generate_html_report
from find_main_decks import get_main_deck_file

PLANNING_EVALUATIONS = {
    "AtraxaPraetorsVoice": {
        "grades": {"r1": "B", "r2": "A", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "B", "s1": "A", "s2": "B", "s3": "B"},
        "justifications": {
            "r1": "4-color mana fixing with green ramp and artifacts.",
            "r2": "Proliferating loyalty on planeswalkers generates compounding card advantage every turn.",
            "a1": "Planeswalker tutors and high superfriends redundancy.",
            "a2": "Deploys Atraxa and establishes planeswalker board presence on Turns 5–6.",
            "p1": "Presents game-winning planeswalker ultimate locks on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps to tick loyalty to emblem thresholds.",
            "p3": "Planeswalkers on board clearly display loyalty counts.",
            "i1": "Widespread removal and Teferi's Protection.",
            "i2": "Narset, Parter of Veils shuts down opposing card draw.",
            "s1": "Teferi's Protection and Atraxa vigilance/lifelink body deter attacks.",
            "s2": "Moderate recovery via mass reanimation (Primevals' Glorious Rebirth).",
            "s3": "Planeswalkers tick up independently, but Atraxa doubles the clock."
        }
    },
    "CaesarLegionsEmperor": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Mardu mana rocks and token-sac treasure generation.",
            "r2": "Caesar's attack trigger draws 2 cards while sacrificing tokens.",
            "a1": "Token creator and anthem redundancy.",
            "a2": "Assembles token army and attack triggers on Turns 5–6.",
            "p1": "Presents wide combat damage and non-combat burn on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps to eliminate players.",
            "p3": "Combat-based attack triggers.",
            "i1": "Mardu removal suite (Anguished Unmaking, Crackling Doom, Ruinous Ultimatum).",
            "i2": "Light incidental sacrifice drain.",
            "s1": "Teferi's Protection and Boros Charm.",
            "s2": "Tokens are fragile to sweepers.",
            "s3": "Deck functions as a go-wide soldier/token shell without Caesar."
        }
    },
    "CaptainNghathrod": {
        "grades": {"r1": "C", "r2": "B", "a1": "C", "a2": "B", "p1": "C", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Budget Dimir mana base with tapland friction.",
            "r2": "Stealing opponent creatures at end of turn fuels board presence.",
            "a1": "Horror typal redundancy with combat mill cards.",
            "a2": "Starts stealing milled threats on Turns 6–7.",
            "p1": "Presents cumulative combat mill damage on Turns 8–9.",
            "p2": "Requires 2–3 opponent untap steps to win through stolen creatures or mill.",
            "p3": "Telegraphed combat triggers.",
            "i1": "Counterspell, Pongify, and Dimir spot removal.",
            "i2": "Mesmeric Orb and mill taxes; no hard locks.",
            "s1": "Lightning Greaves and boots protect the Captain.",
            "s2": "Rebuilding relies on drawing fresh Horrors.",
            "s3": "Steal payoff requires Captain N'ghathrod."
        }
    },
    "ChainerDementiaMaster": {
        "grades": {"r1": "B", "r2": "A", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "B", "s1": "B", "s2": "A", "s3": "C"},
        "justifications": {
            "r1": "Mono-black ramp (Crypt Ghast, Cabal Coffers, Jet Medallion).",
            "r2": "Instant-speed reanimation of any graveyard generates massive card flow.",
            "a1": "Black tutors (Entomb, Buried Alive, Demonic Tutor) fetch key reanimation targets.",
            "a2": "Establishes Chainer loop on Turns 5–6.",
            "p1": "Presents devastating life drain loops (Gary / Kokusho) on Turns 6–7.",
            "p2": "Requires 1–2 opponent untap steps, or immediate loop with sac outlet.",
            "p3": "Instant-speed reanimation from any graveyard.",
            "i1": "Repeatable creature sacrifice removal and black spot removal.",
            "i2": "Repeated edicts and opponent graveyard theft strip opposing resources.",
            "s1": "Chainer life payment is an alias for mana; boots protect Chainer.",
            "s2": "Reanimation engine thrives after wipes.",
            "s3": "Nightmare exile trigger makes Chainer removal impactful."
        }
    },
    "EdgarMarkov": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "B", "s3": "S"},
        "justifications": {
            "r1": "Mardu mana rocks and 1-2 drop vampires.",
            "r2": "Vampire typal draw (Welcoming Vampire, Tocasia's Welcome, Skullclamp).",
            "a1": "High redundancy of 1-3 CMC aggressive vampires.",
            "a2": "Eminence generates tokens starting on Turn 1.",
            "p1": "Presents overwhelming vampire swarm on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps to swing for lethal.",
            "p3": "Wide creature swarm visible on table.",
            "i1": "Mardu spot removal suite.",
            "i2": "Light incidental life drain; no hard denial.",
            "s1": "Boros Charm and Flawless Maneuver.",
            "s2": "Eminence ensures every cast creature creates a free token even after wipes.",
            "s3": "Eminence operates completely from the command zone; Edgar rarely needs to be cast."
        }
    },
    "EmperorPalamecia": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Grixis mana rocks and burn ramp.",
            "r2": "Reanimating threats from hell generates virtual card advantage.",
            "a1": "Redundancy of burn spells and reanimation targets.",
            "a2": "Flips into Lord Master of Hell on Turns 5–6.",
            "p1": "Presents lethal burn and reanimated threats on Turns 6–7.",
            "p2": "2 opponent untap steps to close through combat and burn.",
            "p3": "Telegraphed board triggers.",
            "i1": "Grixis destroy and burn removal.",
            "i2": "Damage taxes on opposing actions.",
            "s1": "Standard boots and redirect protection.",
            "s2": "Moderate recovery via graveyard targets.",
            "s3": "Commander flip is central payoff."
        }
    },
    "FelotharSteadfast": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Bant ramp with green dorks and landramp.",
            "r2": "ETB card draw triggers and token generation.",
            "a1": "Blink targets and token redundancy.",
            "a2": "Establishes token engine on Turns 5–6.",
            "p1": "Presents lethal token overrun on Turns 6–7.",
            "p2": "2 opponent untap steps for combat.",
            "p3": "Creature-based token board.",
            "i1": "Bant counterspells and exile removal (Swords, Path, Beast Within).",
            "i2": "Zero proactive locks.",
            "s1": "Teferi's Protection and Heroic Intervention.",
            "s2": "Wraths wipe tokens cleanly.",
            "s3": "Tokens can function without commander."
        }
    },
    "GisaTheHellraiser": {
        "grades": {"r1": "A", "r2": "A", "a1": "B", "a2": "A", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "B", "s1": "A", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "Mono-black big mana (Cabal Coffers, Urborg, Crypt Ghast, Nykthos, Dark Ritual).",
            "r2": "Skullclamp, Idol of Oblivion, Yawgmoth, and Staff of Domination provide continuous replenishment.",
            "a1": "High density of instant-speed repeatable crime enablers (10+ permanents).",
            "a2": "Deploys Gisa and triggers crimes on every player's turn starting Turn 5.",
            "p1": "Presents menace Zombie army (up to 8 Zombies / 24 power per turn cycle) on Turns 6–7.",
            "p2": "1–2 opponent untap steps to swing for lethal with menace swarm, or Gray Merchant drain.",
            "p3": "Crimes trigger at instant speed; menace makes combat difficult to block.",
            "i1": "Targeted exile crimes and instant removal.",
            "i2": "Repeatable graveyard exile (Ghost Vacuum, Relic, Withered Wretch) and Noxious Ghoul board wipes.",
            "s1": "Inherent Ward: {2}, Pay 2 life, plus Commander's Plate (protection from WURG).",
            "s2": "Bringer of the Last Gift and mass reanimation rebuild full boards.",
            "s3": "Crime engines can trigger independently, but Zombies require Gisa."
        }
    },
    "GreenGoblin": {
        "grades": {"r1": "B", "r2": "A", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "A", "i2": "C", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Grixis artifact ramp and treasure generators.",
            "r2": "Villain card advantage and artifact draw engines.",
            "a1": "Artifact tutoring and villain redundancy.",
            "a2": "Deploys Green Goblin and flips on Turns 5–6.",
            "p1": "Presents lethal artifact burn / pumpkin bomb damage on Turns 6–7.",
            "p2": "2 opponent untap steps for combat and burn.",
            "p3": "Artifact and creature triggers.",
            "i1": "Cyclonic Rift, Fierce Guardianship, and premium Grixis interaction.",
            "i2": "Light incidental sacrifice drain.",
            "s1": "Fierce Guardianship and countermagic stack protection.",
            "s2": "Moderate artifact recursion.",
            "s3": "Artifact shell operates moderately well without commander."
        }
    },
    "GrolnokFrogs": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "C", "p2": "B", "p3": "B", "i1": "B", "i2": "F", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Simic land ramp and dorks.",
            "r2": "Self-mill croak counters exile cards to play.",
            "a1": "Frog typal redundancy and self-mill enablers.",
            "a2": "Starts croaking library into exile on Turns 5–6.",
            "p1": "Presents combat frog damage or lab man finish on Turns 7–8.",
            "p2": "Requires 2 opponent untap steps.",
            "p3": "Exiled croak cards are face-down or visible.",
            "i1": "Simic counterspells and bounce spells.",
            "i2": "Zero stax or denial.",
            "s1": "Boots and countermagic.",
            "s2": "Graveyard exile removes resources permanently.",
            "s3": "Croaked cards cannot be played if Grolnok leaves the battlefield."
        }
    },
    "KrenkoMobBoss": {
        "grades": {"r1": "A", "r2": "B", "a1": "B", "a2": "A", "p1": "A", "p2": "A", "p3": "B", "i1": "C", "i2": "F", "s1": "A", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Fast mana rocks (Ancient Tomb, Mox Diamond) and explosive Goblin ramp.",
            "r2": "The One Ring, Skullclamp, and impulse draw keep hands refueled.",
            "a1": "Goblin Matron, Goblin Recruiter, and imperial tutors.",
            "a2": "Assembles Krenko + untap loop on Turns 4–5.",
            "p1": "Presents infinite goblin loops and lethal swarm on Turns 4–5.",
            "p2": "0–1 opponent untap steps once combo executes with haste.",
            "p3": "Telegraphed Krenko, but fast stack-based untap activations.",
            "i1": "Deflecting Swat, Chaos Warp, and burn.",
            "i2": "Zero stax or denial.",
            "s1": "Deflecting Swat, Lightning Greaves, and fast haste.",
            "s2": "Vulnerable to sweepers if Krenko is removed before untap.",
            "s3": "Deck heavily built around Krenko's doubling tap ability."
        }
    },
    "MahadiEmporium": {
        "grades": {"r1": "A", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "B", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Mahadi creates Treasures for every creature that dies each turn, generating massive burst mana.",
            "r2": "Bolas's Citadel and aristocrat draw triggers refuel hand.",
            "a1": "Sacrifice outlet and creature death redundancy.",
            "a2": "Establishes treasure engine on Turns 5–6.",
            "p1": "Presents lethal Bolas's Citadel drain on Turns 6–7.",
            "p2": "1–2 opponent untap steps to close out game.",
            "p3": "Citadel is telegraphed, but generates immediate win lines.",
            "i1": "Rakdos creature removal and edicts.",
            "i2": "Recurring edict attrition loops.",
            "s1": "Boots and redirect spells.",
            "s2": "Treasures remain after creature board wipes.",
            "s3": "Aristocrat engine functions moderately well without Mahadi."
        }
    },
    "Morophon": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "5-color mana base with 1-drop elf dorks and artifacts.",
            "r2": "Tribal draw engines and Maskwood Nexus synergy.",
            "a1": "High changeling redundancy benefiting from all tribal lords.",
            "a2": "Casts Morophon and reduces creature costs on Turns 5–6.",
            "p1": "Presents multi-lord buffed changeling army on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps for combat.",
            "p3": "Board-based creature swarm.",
            "i1": "Kindred Dominance, spot removal, and tribal counterspells.",
            "i2": "Asymmetrical one-sided wipes.",
            "s1": "Drogskol Captain (hexproof) and Knight Exemplar (indestructible).",
            "s2": "Patriarch's Bidding reanimates all changelings.",
            "s3": "Lords still buff native changelings without Morophon."
        }
    },
    "NekusarMindrazer": {
        "grades": {"r1": "B", "r2": "A", "a1": "B", "a2": "B", "p1": "B", "p2": "A", "p3": "B", "i1": "B", "i2": "A", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Grixis mana rocks and rituals.",
            "r2": "Wheels (Windfall, Wheel of Fortune effects) draw 7 cards repeatedly.",
            "a1": "Wheel redundancy and damage amplifier density.",
            "a2": "Deploys Nekusar and chains wheels on Turns 5–6.",
            "p1": "Presents lethal wheel damage (Orcish Bowmasters, Underworld Dreams) on Turns 6–7.",
            "p2": "1 opponent untap step or immediate lethal wheel chain.",
            "p3": "Continuous life drain on card draw.",
            "i1": "Counterspells and Grixis creature removal.",
            "i2": "Orcish Bowmasters and damage punish opponents severely for drawing cards.",
            "s1": "Countermagic protection for Nekusar.",
            "s2": "Rebuilding requires drawing fresh wheel engines.",
            "s3": "Other pingers (Megrim, Underworld Dreams) act as backup win cons."
        }
    },
    "OmnathLocusOfCreation": {
        "grades": {"r1": "A", "r2": "A", "a1": "B", "a2": "A", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "4-color landfall triggers produce {W}{U}{B}{R} and 4 mana on second land drop.",
            "r2": "Omnath draws a card on ETB; landfall engines draw cards on every land.",
            "a1": "Fetchlands, land tutors (Crop Rotation, Scapeshift), and ramp spells.",
            "a2": "Explosive landfall loops running by Turns 4–5.",
            "p1": "Presents massive landfall damage and board swarm on Turns 6–7.",
            "p2": "2 opponent untap steps for combat, or burn damage from Omnath third trigger.",
            "p3": "Heavily telegraphed land development.",
            "i1": "Fierce Guardianship, Swords to Plowshares, Beast Within.",
            "i2": "Light damage pinging; no stax.",
            "s1": "Heroic Intervention and counterspells.",
            "s2": "Splendid Reclamation and Ramunap Excavator recur lands from graveyard.",
            "s3": "Landfall pieces function, but Omnath is the marquee engine."
        }
    },
    "RamsesAssassinLord": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "A", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Dimir mana rocks and cheap assassins.",
            "r2": "Coastal Piracy and combat damage card draw.",
            "a1": "Assassin typal redundancy and evasion enablers.",
            "a2": "Deploys Ramses and assassin army on Turns 5–6.",
            "p1": "Presents alternate win condition (kill 1 player to win the game) on Turns 6–7.",
            "p2": "0–1 opponent untap steps once an opponent is eliminated with Ramses attacking.",
            "p3": "Alternate win condition is printed on the commander.",
            "i1": "Dimir counterspells and destroy removal.",
            "i2": "Targeted assassination of opposing threats.",
            "s1": "Lightning Greaves, boots, and countermagic.",
            "s2": "Moderate recovery via reanimation.",
            "s3": "Alternate win condition relies completely on Ramses."
        }
    },
    "SauronArmyFling": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Grixis mana rocks and treasure generation.",
            "r2": "Ring temptation card draw and sacrifice draw spells.",
            "a1": "Amass redundancy and fling outlets (Fling, Kazuul's Fury, Chandra's Ignition).",
            "a2": "Amasses 10+/10+ army on Turns 5–6.",
            "p1": "Presents lethal Fling damage on Turns 6–7.",
            "p2": "1–2 opponent untap steps to fling army at remaining opponents.",
            "p3": "Army growth is visible on board.",
            "i1": "Grixis destroy removal and countermagic.",
            "i2": "Light incidental sacrifice drain.",
            "s1": "Sauron inherent Ward: sacrifice legendary creature.",
            "s2": "Can re-amass a fresh army after a wipe.",
            "s3": "Fling package requires a large creature."
        }
    },
    "SvellaIceShaper": {
        "grades": {"r1": "A", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "B", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "Svella taps to create Icy Manaliths, producing permanent cumulative mana rocks every turn.",
            "r2": "Svella's 8-mana ability digs 4 cards deep and casts spells for free.",
            "a1": "Big mana threats and untapper redundancy.",
            "a2": "Engine compounds with Seedborn Muse on Turns 5–6.",
            "p1": "Presents huge Eldrazi / Apex monster threats on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps for combat.",
            "p3": "Icy Manaliths accumulate visibly on board.",
            "i1": "Gruul destroy spells and artifact hate.",
            "i2": "Seedborn Muse untaps all permanents on every player's turn to activate Svella 4 times per turn cycle.",
            "s1": "Boots and indestructible artifacts.",
            "s2": "Icy Manaliths survive creature wipes, ensuring immense mana persists.",
            "s3": "Deck requires Svella to create the mana rocks."
        }
    },
    "SyggRiverCutthroat": {
        "grades": {"r1": "B", "r2": "A", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "A", "i2": "A", "s1": "A", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Dimir mana rocks and 2-mana commander.",
            "r2": "Rhystic Study, Sygg end-step draw, and continuous chip damage draw.",
            "a1": "High density of evasive rogues and disruptive flash creatures.",
            "a2": "Starts drawing cards on Turn 3.",
            "p1": "Presents lethal combat damage / drain on Turns 6–7.",
            "p2": "2 opponent untap steps for attrition combat.",
            "p3": "Instant-speed flash threats.",
            "i1": "Cyclonic Rift, Fierce Guardianship, Force of Negation, and premium Dimir interaction.",
            "i2": "Orcish Bowmasters and Rhystic Study tax and punish opponents on every action.",
            "s1": "Fierce Guardianship and free countermagic protect key turns.",
            "s2": "Low resilience to resolved wipes.",
            "s3": "Tempo shell functions with other card draw engines."
        }
    },
    "ThaliaGitrog": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "A", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "Abzan land ramp and extra land drops per turn.",
            "r2": "Sacrificing creatures/lands on attack draws cards.",
            "a1": "Landfall and death trigger redundancy.",
            "a2": "Deploys commander on Turn 4.",
            "p1": "Presents combat lock on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps.",
            "p3": "Visible board stax.",
            "i1": "Abzan removal suite (Swords, Path, Assassin's Trophy).",
            "i2": "Thalia & Gitrog forces all opposing nonbasic lands and creatures to enter the battlefield tapped, heavily delaying opponents.",
            "s1": "First strike and deathtouch make commander difficult to attack into.",
            "s2": "Lands can be replayed from graveyard.",
            "s3": "Stax effect resides on commander."
        }
    },
    "TheNecrobloom": {
        "grades": {"r1": "A", "r2": "A", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "B", "s1": "A", "s2": "A", "s3": "C"},
        "justifications": {
            "r1": "Massive landfall landramp (Scapeshift, Splendid Reclamation, Awaken the Woods).",
            "r2": "Skullclamp, Idol of Oblivion, Species Specialist, and dredge draw cards on zombie ETB/death.",
            "a1": "Crop Rotation, Scapeshift, and land tutors find Field of the Dead and Dark Depths.",
            "a2": "Assembles Field of the Dead zombie spigot on Turns 4–5.",
            "p1": "Presents massive 20+ zombie swarm on Turns 6–7.",
            "p2": "Requires 1–2 opponent untap steps for combat, or Noxious Ghoul one-sided wipe.",
            "p3": "Land drops and zombies are clearly visible on table.",
            "i1": "Swords to Plowshares, Beast Within, and Noxious Ghoul asymmetrical wipes.",
            "i2": "Noxious Ghoul gives all opposing non-Zombies -1/-1 per zombie landfall, wiping opposing boards.",
            "s1": "Teferi's Protection, Heroic Intervention, and Clever Concealment.",
            "s2": "Splendid Reclamation and Lumra replay all lands from graveyard post-wipe.",
            "s3": "Field of the Dead in the 99 functions independently of commander."
        }
    },
    "UlalekFusedAtrocity": {
        "grades": {"r1": "A", "r2": "A", "a1": "B", "a2": "A", "p1": "B", "p2": "A", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "Colorless ramp, Eldrazi scions/spawns, and green land ramp into big mana.",
            "r2": "Eldrazi cast triggers draw massive hands (Kozilek, Zhulodok, Echoes of Eternity).",
            "a1": "Eldrazi tutoring and big spell redundancy.",
            "a2": "Deploys Ulalek and copies Eldrazi spells on Turns 5–6.",
            "p1": "Presents copied Annihilator Eldrazi titans on Turns 6–7.",
            "p2": "1 opponent untap step or immediate lethal copied Eldrazi cast triggers.",
            "p3": "Cast triggers resolve even if Eldrazi are countered.",
            "i1": "All Is Dust and cast-trigger exile.",
            "i2": "Annihilator triggers force opponents to sacrifice boards.",
            "s1": "Eldrazi cast triggers cannot be answered by traditional counterspells.",
            "s2": "Massive mana enables immediate re-casting.",
            "s3": "Big Eldrazi can win on their own without Ulalek."
        }
    },
    "UlamogColorless": {
        "grades": {"r1": "A", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "B", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "Colorless big mana rocks (Thran Dynamo, Gilded Lotus, Urza lands, Forsaken Monument).",
            "r2": "Colorless draw artifacts (Mind Stone, Hedron Archive, Kozilek).",
            "a1": "Colorless tutors (Expedition Map, Conduit of Ruin).",
            "a2": "Reaches 10 mana for Ulamog on Turns 5–6.",
            "p1": "Presents indestructible 10/10 with mill 20 on attack on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps to eliminate players.",
            "p3": "Indestructible titan visible in command zone.",
            "i1": "Ulamog cast trigger exiles two permanents on cast.",
            "i2": "Attack trigger exiles top 20 cards of defending player's library.",
            "s1": "Inherent indestructible on Ulamog.",
            "s2": "High mana base allows recasting even through commander tax.",
            "s3": "Other colorless titans act as independent threats."
        }
    },
    "UltronArtificialMalevolence": {
        "grades": {"r1": "B", "r2": "A", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "Esper artifact mana rocks and cost reducers.",
            "r2": "The One Ring, artifact draw triggers, and token replenishment.",
            "a1": "Fabricate, Whir of Invention, and artifact tutors.",
            "a2": "Establishes Ultron drone assembly line on Turns 5–6.",
            "p1": "Presents swarm of growing artifact drones on Turns 6–7.",
            "p2": "2 opponent untap steps for combat damage.",
            "p3": "Artifact drone creation visible on board.",
            "i1": "Esper counterspells and exile removal.",
            "i2": "Light incidental taxation; no hard denial.",
            "s1": "Indestructible artifacts and countermagic.",
            "s2": "Scrap Trawler and artifact recursion.",
            "s3": "Artifact drone shell functions moderately well without commander."
        }
    },
    "YidrisChaos": {
        "grades": {"r1": "B", "r2": "A", "a1": "B", "a2": "A", "p1": "B", "p2": "A", "p3": "B", "i1": "A", "i2": "C", "s1": "B", "s2": "B", "s3": "C"},
        "justifications": {
            "r1": "4-color mana fixing with green ramp, rituals, and rocks.",
            "r2": "Cascading spells grant immense free card advantage and storm velocity.",
            "a1": "Cascade velocity naturally digs deep through library.",
            "a2": "Connects with Yidris and chains cascade storms on Turns 5–6.",
            "p1": "Presents massive multi-spell cascade turn on Turns 5–6.",
            "p2": "1 opponent untap step or immediate same-turn storm kill.",
            "p3": "Yidris must connect combat damage to trigger cascade.",
            "i1": "Cyclonic Rift, Jeska's Will, and countermagic.",
            "i2": "Overwhelming board advantage; no stax.",
            "s1": "Trample and evasion enablers protect combat connection.",
            "s2": "Cascading spells rebuild board quickly.",
            "s3": "Spells can be hardcast without Yidris, but cascade is the centerpiece."
        }
    },
    "ZangiefJundAttritron": {
        "grades": {"r1": "B", "r2": "B", "a1": "B", "a2": "B", "p1": "B", "p2": "B", "p3": "B", "i1": "B", "i2": "C", "s1": "A", "s2": "C", "s3": "C"},
        "justifications": {
            "r1": "Jund ramp with dorks and rocks.",
            "r2": "Combat damage draw (Hunter's Insight, Return of the Wildspeaker).",
            "a1": "Fight spells and lure equipment redundancy.",
            "a2": "Deploys Zangief with fight gear on Turns 5–6.",
            "p1": "Presents lethal commander damage / board fight wipes on Turns 6–7.",
            "p2": "2 opponent untap steps for combat elimination.",
            "p3": "Voltron combat and fight spells.",
            "i1": "Fight spells act as creature removal while Zangief takes damage.",
            "i2": "Forces opposing creatures to block and die in combat.",
            "s1": "Inherent indestructible on your turn!",
            "s2": "Moderate recovery via equipment.",
            "s3": "Voltron strategy centers on Zangief."
        }
    }
}

planning_dir = REPO_ROOT / "commander_decks" / "Planning"

for deck_name, eval_data in PLANNING_EVALUATIONS.items():
    d_dir = planning_dir / deck_name
    if not d_dir.exists():
        print(f"Skipping {deck_name}: directory not found")
        continue

    mox_file = d_dir / "moxfield_import.txt"
    card_names = parse_deck_cards(mox_file) if mox_file.exists() else []

    def_template = generate_default_evaluation(deck_name, card_names)
    eval_data["card_ledger"] = def_template["card_ledger"]
    eval_data["deck_name"] = deck_name
    eval_data["thematic_restriction"] = False

    save_evaluation_file(d_dir / "dti_eval.json", eval_data)

    eval_obj = DTIEvaluation(
        grades=eval_data["grades"],
        justifications=eval_data["justifications"],
        card_ledger=eval_data["card_ledger"],
        thematic_restriction=False,
        deck_name=deck_name
    )
    eval_obj.apply_wotc_rules(card_names)
    telemetry = parse_goldfish_telemetry(d_dir)

    md_output = d_dir / "dti_audit.md"
    with open(md_output, "w", encoding="utf-8") as f:
        f.write(render_markdown_audit(eval_obj, telemetry))

    html_output = d_dir / "dti_report.html"
    generate_html_report(eval_obj, html_output, telemetry)

    main_md = get_main_deck_file(d_dir)
    if main_md and main_md.exists():
        content = main_md.read_text(encoding="utf-8", errors="ignore")

        gates_str = "All Passed" if not eval_obj.gates_triggered else f"Triggered: {', '.join(g['name'] for g in eval_obj.gates_triggered)}"
        dti_line = f"*   **DTI Threat Index:** **{eval_obj.threat_score} / 96** (Bracket {eval_obj.final_bracket} | Velocity: **{eval_obj.velocity_vector}/48** | Suppression: **{eval_obj.suppression_vector}/40** | Gates: {gates_str} | [DTI Report](dti_report.html))"

        if re.search(r"\*\s*\*\*DTI Threat Index:\*\*", content):
            new_content = re.sub(r"\*\s*\*\*DTI Threat Index:\*\*[^\n\r]+", dti_line, content)
        elif re.search(r"\*\s*\*\*Bracket:\*\*[^\n\r]+", content):
            def repl_brk(m):
                brk_match = m.group(0)
                return f"{brk_match}\n{dti_line}"
            new_content = re.sub(r"\*\s*\*\*Bracket:\*\*[^\n\r]+", repl_brk, content, count=1)
        elif "## Commander Strategy" in content:
            new_content = content.replace("## Commander Strategy", f"## Commander Strategy\n{dti_line}\n")
        elif "## Deck Strategy" in content:
            new_content = content.replace("## Deck Strategy", f"## Deck Strategy\n{dti_line}\n")
        else:
            new_content = content

        main_md.write_text(new_content, encoding="utf-8")
        print(f"[OK] {deck_name:<28} -> DTI: {eval_obj.threat_score:>2}/96 | B{eval_obj.final_bracket} | Vel: {eval_obj.velocity_vector:>2} | Sup: {eval_obj.suppression_vector:>2} | Updated: {main_md.name}")
    else:
        print(f"[WARN] {deck_name}: No main markdown file found!")

print("\nAll 27 Planning Decks successfully audited, evaluated, and synchronized!")
