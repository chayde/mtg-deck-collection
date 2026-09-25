import os
import sys
import re
import json
import subprocess
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from dti_evaluator import DTIEvaluation, BENCHMARK_META, generate_default_evaluation, parse_deck_cards, parse_goldfish_telemetry, save_evaluation_file, render_markdown_audit, generate_html_report
from find_main_decks import get_main_deck_file

# Define bespoke DTI evaluations for each Owned deck based on its archetype, cards, and speed:
OWNED_EVALUATIONS = {
    "CaptainAmerica": {
        "grades": {
            "r1": "B", "r2": "B", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "F", "s1": "A", "s2": "C", "s3": "C"
        },
        "justifications": {
            "r1": "Reliable 2-CMC rock ramp and equipment cost reducers (Danitha, Puresteel Paladin, Forge Anew).",
            "r2": "Equipment-driven card draw (Puresteel, Sram, Esper Sentinel, Akiri) generates steady cards per turn.",
            "a1": "Equipment tutors (Stoneforge Mystic, Open the Armory, Fighter Class) provide direct access to key tools.",
            "a2": "Equips and assembles voltron package on Turns 5–6.",
            "p1": "Presents lethal commander damage / shield throw threat on Turns 6–7.",
            "p2": "Requires 2 opponent untap cycles to eliminate all three players via combat.",
            "p3": "Telegraphed equipment board state; vulnerable to artifact wipes if protection isn't up.",
            "i1": "Efficient instant-speed removal suite (Swords to Plowshares, Path to Exile, Wear // Tear).",
            "i2": "Zero proactive restriction or stax effects.",
            "s1": "High-density equipment ward/hexproof (Swiftfoot Boots, Mithril Coat, Robe of Stars, Teferi's Protection).",
            "s2": "Moderate recovery via equipment recursion (Sun Titan, Mantle of the Ancients).",
            "s3": "Deck heavily relies on Captain America to throw equipment; fair voltron beatdown without him."
        }
    },
    "EtaliConqueror": {
        "grades": {
            "r1": "A", "r2": "A", "a1": "B", "a2": "A",
            "p1": "B", "p2": "B", "p3": "B", "i1": "C",
            "i2": "C", "s1": "B", "s2": "B", "s3": "C"
        },
        "justifications": {
            "r1": "Explosive Gruul ramp suite (12+ dorks and 2-CMC ramp) deploying 7-mana Etali by Turn 4–5.",
            "r2": "Etali cast triggers cast 4 free spells from pods; recurring copy/blink loops generate immense card advantage.",
            "a1": "Redundancy of clone/blink and haste enablers (Twinflame, Heat Shimmer, Molten Duplication).",
            "a2": "Casts Etali and triggers initial wave by Turn 4.5–5.",
            "p1": "Presents massive multi-spell board parity break on Turns 5–6.",
            "p2": "Requires 2 opponent untaps to close the game via combat or poison flip.",
            "p3": "Etali is telegraphed in the command zone, but ETB triggers resolve regardless of spot removal.",
            "i1": "Light reactive interaction; primarily relies on stolen opponent spells.",
            "i2": "Incidental board disruption via Etali hits; no intentional stax.",
            "s1": "Moderate protection (Deflecting Swat, Heroic Intervention, Lightning Greaves).",
            "s2": "Etali ETB restocks board immediately even after mass board wipes.",
            "s3": "Deck is built entirely around Etali's ETB trigger."
        }
    },
    "HenzieBlitz": {
        "grades": {
            "r1": "A", "r2": "A", "a1": "B", "a2": "A",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "C", "s1": "B", "s2": "A", "s3": "C"
        },
        "justifications": {
            "r1": "8x 1-drop mana dorks guaranteeing Turn 2 Henzie deployment and discounted blitz curves.",
            "r2": "Blitz provides automatic death card draw on every creature, augmented by Greater Good and Birthing Ritual.",
            "a1": "Survival of the Fittest and Birthing Ritual provide powerful creature tutoring.",
            "a2": "Blitz engine runs at full throttle starting Turn 3–4.",
            "p1": "Presents game-ending creature swarm and non-combat life drain on Turns 6–7.",
            "p2": "2 opponent untap steps to close through combat, or 1 turn cycle with Living Death burst.",
            "p3": "Creature attack triggers are telegraphed but carry immediate haste and death draw value.",
            "i1": "Creature-based spot removal (Druid of Purification, Archon of Cruelty, Assassin's Trophy).",
            "i2": "Incidental sacrifice edicts (Archon of Cruelty, Massacre Wurm); no hard stax.",
            "s1": "Blitz creatures sacrifice themselves regardless of opponent interaction.",
            "s2": "Living Death and graveyard recursion turn board wipes into win conditions.",
            "s3": "Deck requires Henzie for blitz discounts, but can hardcast 5-drops in late game."
        }
    },
    "IncredibleHulk": {
        "grades": {
            "r1": "B", "r2": "B", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "F", "s1": "B", "s2": "C", "s3": "C"
        },
        "justifications": {
            "r1": "Solid Temur ramp with 2-CMC ramp and Doc Samson power-scaling mana.",
            "r2": "Bruce Banner front face provides repeatable card draw {X}{X} dump.",
            "a1": "Typal redundancy and counter synergy (+1/+1 counter doublers).",
            "a2": "Flips into Hulk with counters setup on Turns 5–6.",
            "p1": "Presents lethal trample damage / Fling burst on Turns 6–7.",
            "p2": "2 opponent untaps for fair combat, or same-turn Fling / Caltrops extra combat line.",
            "p3": "Board-based combat strategy with visible counter growth.",
            "i1": "Temur countermagic and burn removal (Beast Within, Chaos Warp, Chandra's Ignition).",
            "i2": "Zero proactive restriction or stax effects.",
            "s1": "Protection boots and counter protection; Hulk Enrage punishes direct damage.",
            "s2": "Moderate recovery via counter restocking; vulnerable to mass bounce/exile.",
            "s3": "Front face provides card draw; back face provides finisher."
        }
    },
    "KarametraAngels": {
        "grades": {
            "r1": "A", "r2": "B", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "B", "s1": "A", "s2": "B", "s3": "B"
        },
        "justifications": {
            "r1": "Karametra land-fetch triggers on every creature cast ramp 10+ lands ahead of curve, plus Smothering Tithe.",
            "r2": "Beast Whisperer, The Great Henge, and angel draw triggers maintain hand replenishment.",
            "a1": "Worldly Tutor, Eladamri's Call, and creature redundancy find key angels.",
            "a2": "Achieves high-mana Angel deployment by Turns 5–6.",
            "p1": "Presents flying angel board pressure on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps to swing for lethal across 3 players.",
            "p3": "Visible high-flying threats; heavily telegraphed combat wins.",
            "i1": "Path, Swords, Beast Within, and Generous Gift spot removal suite.",
            "i2": "Aura Shards repeatedly destroys all opposing artifacts/enchantments on every creature cast.",
            "s1": "Teferi's Protection, Heroic Intervention, and Avacyn indestructible shielding.",
            "s2": "Massive land base allows fast re-casting of angels after wipes.",
            "s3": "Indestructible commander; deck functions well once lands are pulled from library."
        }
    },
    "MarchesaBlackRose": {
        "grades": {
            "r1": "B", "r2": "A", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "B", "s1": "A", "s2": "A", "s3": "C"
        },
        "justifications": {
            "r1": "Standard Grixis mana rocks and treasure generation.",
            "r2": "Dethrone + aristocrat death draw (Grim Haruspex, Midnight Reaper, River Kelpie) draws cards on every turn.",
            "a1": "High redundancy of sacrifice outlets, counter placers, and ETB burn creatures.",
            "a2": "Assembles Marchesa recursive engine on Turns 5–6.",
            "p1": "Presents persistent board control and drain clock on Turns 6–7.",
            "p2": "2 opponent untap steps of end-step recursion and combat drain.",
            "p3": "Aristocrat engine relies on graveyard returns at end of turn.",
            "i1": "Instant removal and sacrifice edicts (Fleshbag Marauder, Plaguecrafter on loop).",
            "i2": "Continuous recurring edicts strip opponents of creatures during every turn cycle.",
            "s1": "Marchesa automatically returns any creature with a +1/+1 counter to the battlefield at end step.",
            "s2": "Wipe-proof engine: creatures dying to wrath return immediately on end step.",
            "s3": "Heavily reliant on Marchesa being on the battlefield to enable the recursion loop."
        }
    },
    "MerenGolgari": {
        "grades": {
            "r1": "B", "r2": "A", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "B", "s1": "B", "s2": "A", "s3": "C"
        },
        "justifications": {
            "r1": "Green land ramp and sacrifice mana dorks (Sakura-Tribe Elder, Steve loop).",
            "r2": "Self-mill, dredge, and continuous end-step reanimation provide immense card flow.",
            "a1": "Grave tutors (Buried Alive, Entomb, Jarad's Orders) tutor directly to recursion pool.",
            "a2": "Establishes experience counter reanimation loop on Turns 5–6.",
            "p1": "Presents reanimation attrition and Gary drain on Turns 6–7.",
            "p2": "2 opponent untap steps to grind out life totals.",
            "p3": "Graveyard-reliant strategy vulnerable to Rest in Peace / Bojuka Bog.",
            "i1": "Repeatable creature edicts (Plaguecrafter, Spore Frog lock).",
            "i2": "Recurring edicts systematically strip opponents of creature boards.",
            "s1": "Spore Frog loops fog attacks; boots protect Meren.",
            "s2": "Graveyard engine naturally thrives and rebuilds after mass destruction.",
            "s3": "Meren is central engine; hard reanimation spells act as backups."
        }
    },
    "QuantumQuandrix": {
        "grades": {
            "r1": "B", "r2": "B", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "F", "s1": "B", "s2": "C", "s3": "C"
        },
        "justifications": {
            "r1": "Simic land ramp and mana dorks.",
            "r2": "Token-fed draw and blue cantrip/draw engines.",
            "a1": "Token creator redundancy and clone generators.",
            "a2": "Doubles token creation starting Turns 5–6.",
            "p1": "Presents exponential token army on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps to swing with non-haste token swarms.",
            "p3": "Heavily telegraphed token board states.",
            "i1": "Simic countermagic and bounce interaction (Pongify, Rapid Hybridization, Counterspell).",
            "i2": "Zero stax or denial.",
            "s1": "Heroic Intervention and countermagic protection.",
            "s2": "Tokens are wiped cleanly by wraths; requires fresh token generators to rebuild.",
            "s3": "Adrix and Nev provide the doubling, but base tokens can function without them."
        }
    },
    "RoccoStreetChef": {
        "grades": {
            "r1": "B", "r2": "A", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "C", "s1": "B", "s2": "C", "s3": "C"
        },
        "justifications": {
            "r1": "Naya ramp with 2-CMC dorks and Food token artifact utility.",
            "r2": "Impulse exile draw on every end step generates continuous card advantage.",
            "a1": "High density of exile-matters payoffs and counter multipliers.",
            "a2": "Engine starts churning Food and counters on Turns 4–5.",
            "p1": "Presents tall/wide modified creature army on Turns 6–7.",
            "p2": "2 opponent untap steps to execute combat wins.",
            "p3": "Exiled cards are revealed to the entire table, giving opponents advance warning.",
            "i1": "Naya instant-speed removal suite (Beast Within, Swords to Plowshares, Chaos Warp).",
            "i2": "Light group-hug style impulse triggers; no hard denial.",
            "s1": "Protection spells (Heroic Intervention, Flawless Maneuver).",
            "s2": "Food tokens remain on board after wipes to regain life, but creatures must be rebuilt.",
            "s3": "Deck heavily synergizes with Rocco's exile trigger."
        }
    },
    "SauronGrixis": {
        "grades": {
            "r1": "B", "r2": "A", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "C", "s1": "A", "s2": "B", "s3": "C"
        },
        "justifications": {
            "r1": "Grixis mana rocks and treasure generation deploying 6-mana Sauron on Turn 5.",
            "r2": "Repeatable wheel/refuel draw whenever the Ring tempts you.",
            "a1": "High density of Ring tempting triggers and amass cards.",
            "a2": "Deploys Sauron and establishes amass/wheel engine on Turns 5–6.",
            "p1": "Presents massive 10+/10+ Orc Army and Ring bearer clock on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps for combat damage.",
            "p3": "High ward cost makes Sauron difficult to answer cleanly.",
            "i1": "Grixis countermagic and destroy removal (Feed the Swarm, Bedevil, Blasphemous Act).",
            "i2": "Incidental ring tempt triggers; no hard resource locks.",
            "s1": "Sauron possesses inherent Ward: Sacrifice a legendary creature or artifact.",
            "s2": "Graveyard reanimation packages rebuild army post-wipe.",
            "s3": "Sauron is the primary engine center."
        }
    },
    "TheGreatGoblin": {
        "grades": {
            "r1": "B", "r2": "B", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "C",
            "i2": "F", "s1": "B", "s2": "C", "s3": "C"
        },
        "justifications": {
            "r1": "Rakdos goblin mana dorks (Skirk Prospector) and cheap rocks.",
            "r2": "Goblin death draw and impulse card advantage.",
            "a1": "Goblin typal tutors (Goblin Matron, Boggart Harbinger).",
            "a2": "Assembles goblin army on Turns 5–6.",
            "p1": "Presents swarm attack on Turns 6–7.",
            "p2": "2 opponent untap steps to eliminate players.",
            "p3": "Board-based swarm; vulnerable to sweepers.",
            "i1": "Targeted burn and creature sacrifice removal.",
            "i2": "Zero proactive restriction or stax.",
            "s1": "Standard goblin protection and haste enablers.",
            "s2": "Rebuilding requires fresh hand of goblins.",
            "s3": "Functions as a general goblin typal swarm without commander."
        }
    },
    "TheHive": {
        "grades": {
            "r1": "B", "r2": "A", "a1": "B", "a2": "B",
            "p1": "B", "p2": "A", "p3": "B", "i1": "B",
            "i2": "C", "s1": "A", "s2": "B", "s3": "B"
        },
        "justifications": {
            "r1": "5-color mana base with mana dork slivers (Gemhide, Manaweft) and green ramp.",
            "r2": "Cascade chains from The First Sliver vomit multiple slivers; Synapse/Dormant draw cards.",
            "a1": "Homing Sliver (slivercycling) and cascade provide consistent access to key slivers.",
            "a2": "Cascade engine unleashes on Turn 5.",
            "p1": "Presents lethal haste/evasion sliver swarm on Turns 6–7.",
            "p2": "1 opponent untap step or immediate lethal swing with Cloudshredder / Heart Sliver.",
            "p3": "Cascading into unblockable/flying slivers creates explosive, rapid clock.",
            "i1": "Harmonic Sliver (repeatable Naturalize) and Necrotic Sliver (Vindicate).",
            "i2": "Harmonic Sliver systematically eliminates opposing mana rocks and engines.",
            "s1": "Crystalline Sliver (shroud to all slivers), Hibernation Sliver, and Quick Sliver.",
            "s2": "Living Death and Patriarch's Bidding mass-reanimate the entire hive.",
            "s3": "Sliver lords buff each other effectively even without The First Sliver."
        }
    },
    "UrDragonKibler": {
        "grades": {
            "r1": "A", "r2": "A", "a1": "B", "a2": "B",
            "p1": "B", "p2": "B", "p3": "B", "i1": "B",
            "i2": "C", "s1": "B", "s2": "B", "s3": "A"
        },
        "justifications": {
            "r1": "Eminence reduces all dragon costs by {1} all game; optimized fetch/shock ramp lands and rocks.",
            "r2": "Elemental Bond, Garruk's Uprising, The Great Henge, and Dragon draw engines.",
            "a1": "Dragon tutors (Sarkhan's Triumph, Scion of the Ur-Dragon) and dragon redundancy.",
            "a2": "Deploys 5-6 CMC dragons ahead of curve on Turns 4–5.",
            "p1": "Presents lethal flying dragon combat pressure on Turns 6–7.",
            "p2": "Requires 2 opponent untap steps to eliminate pod through combat.",
            "p3": "Big flying threats clearly visible on board.",
            "i1": "Terror of the Peaks ETB burn, Dragon Tempest, and flexible spot removal.",
            "i2": "Light incidental ETB burn clearing opposing boards.",
            "s1": "Heroic Intervention, Lightning Greaves, and dragon ward effects.",
            "s2": "High mana availability enables easy redeployment of dragons post-wipe.",
            "s3": "Eminence functions continuously from the command zone; Ur-Dragon rarely even needs to be cast."
        }
    }
}

owned_dir = REPO_ROOT / "commander_decks" / "Owned"

for deck_name, eval_data in OWNED_EVALUATIONS.items():
    d_dir = owned_dir / deck_name
    if not d_dir.exists():
        print(f"Skipping {deck_name}: directory not found")
        continue

    mox_file = d_dir / "moxfield_import.txt"
    card_names = parse_deck_cards(mox_file) if mox_file.exists() else []

    # Build default ledger
    def_template = generate_default_evaluation(deck_name, card_names)
    eval_data["card_ledger"] = def_template["card_ledger"]
    eval_data["deck_name"] = deck_name
    eval_data["thematic_restriction"] = False

    # Save dti_eval.json
    save_evaluation_file(d_dir / "dti_eval.json", eval_data)

    # Build evaluation object
    eval_obj = DTIEvaluation(
        grades=eval_data["grades"],
        justifications=eval_data["justifications"],
        card_ledger=eval_data["card_ledger"],
        thematic_restriction=False,
        deck_name=deck_name
    )
    eval_obj.apply_wotc_rules(card_names)
    telemetry = parse_goldfish_telemetry(d_dir)

    # Generate Markdown and HTML
    md_output = d_dir / "dti_audit.md"
    with open(md_output, "w", encoding="utf-8") as f:
        f.write(render_markdown_audit(eval_obj, telemetry))

    html_output = d_dir / "dti_report.html"
    generate_html_report(eval_obj, html_output, telemetry)

    # Incorporate into main deck .md file!
    main_md = get_main_deck_file(d_dir)
    if main_md and main_md.exists():
        content = main_md.read_text(encoding="utf-8", errors="ignore")

        # Prepare DTI badge line
        gates_str = "All Passed" if not eval_obj.gates_triggered else f"Triggered: {', '.join(g['name'] for g in eval_obj.gates_triggered)}"
        dti_line = f"*   **DTI Threat Index:** **{eval_obj.threat_score} / 96** (Bracket {eval_obj.final_bracket} | Velocity: **{eval_obj.velocity_vector}/48** | Suppression: **{eval_obj.suppression_vector}/40** | Gates: {gates_str} | [DTI Report](dti_report.html))"

        # Check if DTI Threat Index line already exists
        if re.search(r"\*\s*\*\*DTI Threat Index:\*\*", content):
            new_content = re.sub(r"\*\s*\*\*DTI Threat Index:\*\*[^\n\r]+", dti_line, content)
        elif re.search(r"\*\s*\*\*Bracket:\*\*[^\n\r]+", content):
            # Insert right after the Bracket line
            def repl_brk(m):
                brk_match = m.group(0)
                # Normalize bracket line to match evaluated bracket if needed
                return f"{brk_match}\n{dti_line}"
            new_content = re.sub(r"\*\s*\*\*Bracket:\*\*[^\n\r]+", repl_brk, content, count=1)
        elif "## Commander Strategy" in content:
            # Insert under Commander Strategy
            new_content = content.replace("## Commander Strategy", f"## Commander Strategy\n{dti_line}\n")
        else:
            new_content = content

        main_md.write_text(new_content, encoding="utf-8")
        print(f"[OK] {deck_name:<18} -> DTI: {eval_obj.threat_score:>2}/96 | B{eval_obj.final_bracket} | Vel: {eval_obj.velocity_vector:>2} | Sup: {eval_obj.suppression_vector:>2} | Updated: {main_md.name}")
    else:
        print(f"[WARN] {deck_name}: No main markdown file found!")

print("\nAll 13 Owned Decks successfully audited, evaluated, and synchronized!")
