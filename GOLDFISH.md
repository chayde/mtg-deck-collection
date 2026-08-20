# Goldfish Testing Protocol

This file defines the protocol for running goldfish simulations on Commander decks in this repository. All simulations use `scripts/multiplayer_goldfish.py` — a fully automated 4-player pod simulator powered by Scryfall card classification.

> **API Reference:** All card lookups follow the rules in `API_REFERENCE.md`. The goldfish script uses its own local cache at `scripts/.card_cache.json` and respects Scryfall rate limits automatically.

> ⚠️ **MANDATORY AGENT RULE — BRACKET SELECTION:**
> The `--bracket X` switch is **MANDATORY** for all goldfish simulation commands. The bracket determines the deck's expected engine readiness turn window ($T_{\text{target}}$) per [`BRACKETS.md`](BRACKETS.md).
> **If the target Bracket (1–5) for a deck is not specified in the deck file or is unknown for whatever reason, YOU MUST STOP AND ASK THE USER FOR CLARIFICATION BEFORE RUNNING THE SIMULATION.**

---

## The Script

```bash
python scripts/multiplayer_goldfish.py <deck_file> --bracket <1-5> [--sims N] [--turns N] [--tapped F]
```

**Arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `deck_file` | required | Path to the deck's `moxfield_import.txt` file |
| `--bracket X` | **required** | Target Commander Bracket: `1` (Exhibition, T10), `2` (Core, T9), `3` (Upgraded, T7), `4` (Optimized, T5), `5` (cEDH, T1-3). |
| `--sims N` | 1 | Number of simulations to run (use 20+ for meaningful statistics) |
| `--turns N` | 15 | Number of turns to simulate per game |
| `--tapped F` | 0.60 | Fraction of opponent lands assumed tapped (for Mana Geyser-style cards) |
| `--commander-back` | off | For a **transform DFC commander**, measure deployment of the BACK face (its hard-cast / flip cost) instead of the cheap front face |
| `--commander-cost "{..}"` | none | Manually override the commander cost used for the cast check, e.g. `"{2}{R}{R}{G}{G}"`. Takes priority over `--commander-back` |
| `--html [PATH]` | off | Also write a formatted, self-contained **HTML report** (summary stat cards, a distribution bar chart, and a per-sim table). With no PATH, auto-names `goldfish_report_<timestamp>.html` next to the deck file |

**Example — standard 20-sim run:**
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Planning/Morophon/morophon_changeling_moxfield_import.txt" --sims 20 --turns 10 --bracket 3
```

### Flip / Double-Faced Commanders
For a transform DFC commander whose meaningful threat is the **back** face (e.g. **Bruce Banner // The Incredible Hulk** — a {U} front that flips/hard-casts into a `{2}{R}{R}{G}{G}` back), the default run only measures dropping the cheap front face, which is not the real deployment clock. The simulator auto-detects these and prints a `[commander] NOTE:` telling you to rerun with `--commander-back` (uses the back face's cost) or `--commander-cost "{..}"` (any explicit cost). Log both numbers when relevant: the front tells you when the early-game piece lands, the back tells you when the payoff comes online.
```bash
python scripts/multiplayer_goldfish.py "commander_decks/Owned/IncredibleHulk/moxfield_import.txt" --sims 20 --turns 12 --bracket 4 --commander-back
```

---

## How It Works

The script auto-classifies every card via Scryfall on first run (results cached locally — subsequent runs are instant). It auto-detects lands, ramp, dorks/rocks, burst mana, **enablers** (cheap draw/tutors/engine setup), and **payoffs** (high CMC or win-cons). It then simulates a full 4-player pod with one copy of the deck per seat.

**Each turn, the engine prioritizes:**
1. Play a land (untapped duals first, then untapped singles, tapped last)
2. Cast mana permanents (rocks, dorks) while affordable
3. Cast ramp spells while affordable
4. Cast the commander from the command zone if mana allows
5. Cast generic spells (enablers, payoffs) with remaining mana

**Smart Synergy-Aware Mulligan Logic:**
Evaluating opening hands goes beyond land counts. Hands with 3+ lands but 0 ramp and 0 enablers (all expensive payoffs) are flagged as **Synergy Traps** and mulliganed.
* **Gold Keep:** 2–4 lands + at least 1 ramp/rock + at least 1 enabler.
* **Silver Keep:** 2–5 lands + good mana curve.
* **Desperation Keep:** Forced mulligan down to 5 cards or fewer.

**Pod assumptions:**
- All 4 players run the same deck — opponents' lands cover the full color identity
- Exotic Orchard and Fellwar Stone produce any color (opponents have all 5 colors)
- Mana Geyser scales with opponent tapped lands using the `--tapped` fraction
- Commander tax is tracked and applied on subsequent casts

---

## Deck File Format

The script requires `COMMANDER:` and `DECK:` section headers. The standard `moxfield_import.txt` format already satisfies this:

```text
COMMANDER:
1 Morophon, the Boundless

DECK:
1 Sol Ring
1 Command Tower
...
```

---

## Running a Goldfish Session

Default recommendation for a new deck or after significant changes:

```bash
python scripts/multiplayer_goldfish.py "<path_to_moxfield_import.txt>" --sims 20 --turns 10 --bracket <1-5>
```

For a quick sanity check (single verbose game showing every turn):
```bash
python scripts/multiplayer_goldfish.py "<path_to_moxfield_import.txt>" --sims 1 --turns 10 --bracket <1-5>
```

---

## Reading the Output

**Aggregate Output Block:**
```text
--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 20/20 (100%)
  Commander Cast Range: T4 - T9
  Commander Cast Avg:   T5.8

  Opening Hand Quality Breakdown (20 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   14/20 (70%)
    Silver Keep (Mana + Curve):          5/20 (25%)
    Desperation Keep (Mulligan to <=5):   1/20 (5%)
    Average Starting Hand Size:          6.85 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 19/20 (95%)
  Engine Readiness Avg:  T6.1
  
  [BRACKET COMPLIANCE CHECK] Status: PASS
  Deck hits engine readiness consistently around Turn 6.1, aligning with Bracket 3 (Upgraded) expectations.
```

* **Gold Keep Rate & Avg Hand Size:** High Gold Keep % and Avg Hand Size $>6.7$ indicate a healthy opening hand synergy structure. High desperation keeps suggest land or enabler drought.
* **Engine Readiness:** Measures when the seat has deployed its Commander, cast an Enabler/drawn extra cards, and achieved target mana thresholds.
* **Bracket Compliance Check:** Flags `PASS` if aligned with bracket target turn, or `WARNING (Over-performing)` if the deck hits engine readiness $\ge 1.5$ turns earlier than its bracket target (indicating potential power level leakage).

---

## Logging Results

After running a session, append results to `GOLDFISH_LOG.md` in the deck's directory. Each session gets a dated header. Do not overwrite prior sessions.

```markdown
## [YYYY-MM-DD] — [Test goal] ([N] sims, T[X] turns, Bracket [X])

**Command:**
```
python scripts/multiplayer_goldfish.py "..." --sims N --turns N --bracket X
```

**Results:**
[Paste the full aggregate output block from the script]

**Notes:**
[Any observations about what the data shows — patterns, concerns, recommendations]
```

---

## Cache

The script maintains its own card classification cache at `scripts/.card_cache.json`. This is committed to the repo so cached lookups are shared across machines. First run on a new deck fetches from Scryfall; all subsequent runs are instant.

If you need to force a fresh classification for a card (e.g. after an errata), delete its entry from `scripts/.card_cache.json` manually.
