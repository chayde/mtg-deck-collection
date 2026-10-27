---
name: elephant-minnow
description: >-
  Spec-Driven MTG Commander Deck Engineering & Adversarial Review skill modeled
  on Google's Elephant-Goldfish Model (EGM). Coordinates the long-memory
  Elephant session and stateless, zero-context Minnow subagents across 5
  workflows: emm-brainstorm, emm-draft, emm-review, emm-resolve, and
  emm-drift-report. Use whenever designing a new Commander deck, planning a
  major overhaul (5+ card swaps), stress-testing a candidate 100-card list with
  a Cold Comprehension Check, or auditing deck files for documentation drift.
---

# The Elephant-Minnow Model (EMM) for MTG Commander Deck Engineering

Adapted directly from Google's open-source **Elephant-Goldfish Model** ([`google/elephant-goldfish-model`](https://github.com/google/elephant-goldfish-model)), renamed **Elephant-Minnow (EMM)** so "Goldfish" remains exclusively reserved for our 4-player pod simulator (`scripts/multiplayer_goldfish.py`).

EMM separates deck engineering into two distinct cognitive roles coordinated by the human deckbuilder:
1. **The Elephant (Long-Memory Architect — Main Session):** Holds the deep repository context ([`GEMINI.md`](../../../GEMINI.md), [`history.md`](../../../history.md), [`DeckShapeReferenceGuide.md`](../../../DeckShapeReferenceGuide.md), [`DTI_FRAMEWORK.md`](../../../DTI_FRAMEWORK.md), and user playstyle preferences). During ideation and drafting, **the Elephant does not jump straight to a finished 100-card list**; it interviews the user, stress-tests assumptions, writes structured specs, and later arbitrates Minnow critiques.
2. **The Minnows (Stateless Zero-Context Subagents):** Ephemeral, strictly read-only `research` subagents launched via `invoke_subagent` with **zero memory of the design conversation**. Because they cannot read between the lines or rely on shared chat enthusiasm, they act as cold, objective, adversarial reviewers.

---

## 1. Universal Execution Constraints for the Elephant (CRITICAL)

1. **The Information Firewall (MANDATORY):** When spawning Minnow subagents for `emm-review`, you **MUST NOT** pass the deck's `.md` strategy guide, narrative explanations, or `--reason` strings. Run `python scripts/minnow_prep.py "<deck_dir>" --pack` first and pass **ONLY** `<deck_dir>/minnow_blind_spec.txt` (raw 100 cards + verified Scryfall Oracle text). A review that reads the sales pitch is not a Minnow review.
2. **Artifact-First Delivery:** Never dump massive concept briefs, overhaul specs, or raw multi-agent review reports as walls of text in chat. Write them to disk (`concepts_brief.md`, `design_draft.md`, `minnow_review_report.md`, `minnow_report.html`) and provide a clickable link in chat.
3. **Default to Stress-Testing & Critique First:** Never agree by default. Lead with what is fragile, missing, or risky in a proposed card package or archetype before highlighting its merits.
4. **No Glazing (Anti-Sycophancy):** Eliminate flattering filler (*"brilliant," "great," "smart," "perfect," "spot-on"*). Compliments without mechanical substance are noise.
5. **Generate Counter-Arguments:** For every strategy or synergy package proposed, actively outline: *What is the strongest counter-argument? How does this fold in a real 4-player pod when the Commander is removed twice?*
6. **Owner Decides Architecture:** When a Commander or overhaul has more than one defensible architectural direction (e.g., three distinct Geometric Shapes or sub-themes), present up to 3 options—each with its **3-Step Keystone**, **trade-offs**, and **failure conditions**—and ask the user to choose via a single-select gate (`ask_question` with `len(questions) == 1` and `is_multi_select: false`, without `(Recommended)` prefixes).

---

## 2. Trigger Thresholds (When to Use EMM)

* **Full EMM Lifecycle (`brainstorm` $\rightarrow$ `draft` $\rightarrow$ `review` $\rightarrow$ `resolve`):**
  * Building a **brand-new Commander deck** in `commander_decks/Planning/`.
  * Executing a **major overhaul (5+ card swaps)** or changing a deck's Bracket or Geometric Shape.
* **Direct Review + Resolve (`emm-review` $\rightarrow$ `emm-resolve`):**
  * Auditing an existing 100-card candidate baseline (e.g., an LGS list, precon adaptation, or newly imported deck) before purchasing singles on Manapool.
* **Skip EMM:**
  * Routine 1–4 card tweaks (use `scripts/swap_matrix.py` directly).

---

## 3. The 6 Polymorphic Minnow Personas (`agents/`)

All Minnow personas live in `.agents/skills/elephant-minnow/agents/` and operate in either `Mode: BRAINSTORM` (upstream concept stress-testing) or `Mode: REVIEW` (downstream blind-spec auditing):

| Minnow Persona | File | Core Focus |
| :--- | :--- | :--- |
| **`emm-zoom-out`** | [`agents/zoom_out.md`](agents/zoom_out.md) | **Skeptical Deck Architect:** Enforces YAGNI, [`DeckShapeReferenceGuide.md`](../../../DeckShapeReferenceGuide.md) geometry, **Commander Subtraction**, and flags "Orphan Sub-Packages" ($<6$ cards). |
| **`emm-comprehension`** | [`agents/comprehension.md`](agents/comprehension.md) | **Cold Naive Reader:** Reads *only* `minnow_blind_spec.txt` (zero strategy prose) and must reverse-engineer the **3-Step Keystone**, **Deck Shape**, and **Target Bracket** cold. |
| **`emm-design-critic`** | [`agents/design_critic.md`](agents/design_critic.md) | **Hostile Rules & Pod Adversary:** Hunts for rules nonbos (CR 302.6, *Shroud* vs. Equipment, exile vs. `dies`), "Synergy Bricks" when the Commander is taxed out, and pod interaction blind spots. |
| **`emm-codebase-details`** | [`agents/codebase_details.md`](agents/codebase_details.md) | **Legality, Collection & Preference Auditor:** Audits 100-card singleton rules, color identity, Bracket Game Changers/MLD, `collection.csv` reuse, and user bans (zero filter lands, zero filter Signets). |
| **`emm-readiness`** | [`agents/readiness.md`](agents/readiness.md) | **Execution & Acquisition Gatekeeper:** Verifies `swap_matrix.py` readiness, 20-game Goldfish telemetry (`GOLDFISH_LOG.md`), and DTI Gatekeepers (`dti_eval.json`) before Manapool acquisition. |
| **`emm-synthesizer`** | [`agents/synthesizer.md`](agents/synthesizer.md) | **Swarm Compiler:** Coordinates parallel Minnows, deduplicates overlapping critiques, normalizes severities (`Blocker | Major | Nit`), and compiles reports. |

---

## 4. The 5 EMM Workflows

### Workflow 1: `emm-brainstorm` (Upstream Ideation & Concept Stress-Test)

1. **Multi-Turn Open-Ended Drilling (No 100-Card List Yet):**
   * Drill down via open-ended questions in chat (do NOT use `ask_question` during exploration) until the **Commander**, **Target Bracket (1–5)**, **3-Step Keystone** (Primary Action $\rightarrow$ Capitalization $\rightarrow$ Finisher), **Commander Role/Shape** (Diamond, Inverted Triangle, Pointed Rectangle, Pillar-Shifted), and **Explicit Non-Goals** are clear.
2. **Anchored Hypothesis Readiness Gate:**
   * Summarize the working deck hypothesis in 2–3 sentences and present a single-select gate (`ask_question`):
     * `Review concept with Minnow Swarm`
     * `Clarify additional constraints or goals in chat`
3. **Parallel Minnow Brainstorm Swarm:**
   * Spawn `research` subagents instructed to read the persona files in `.agents/skills/elephant-minnow/agents/` with `Mode: BRAINSTORM` on the anchored hypothesis.
   * Synthesize findings into `<deck_dir>/concepts_brief.md` with sections: `## Overview`, `## Multi-Lens Minnow Analysis`, `## Goals vs. Out-of-Scope Non-Goals`, and `## Key Architectural Decisions`.

---

### Workflow 2: `emm-draft` (Deck Design Spec / Overhaul Spec Construction)

Drafts `<deck_dir>/design_draft.md` iteratively before committing to the final 100-card files:
1. **Section 1 — Overview, 3-Step Keystone & Explicit Non-Goals:** Documents the proactive win path and what the deck explicitly refuses to run.
2. **Section 2 — Deck Shape Geometry & Target DTI Profile:** Applies **Commander Subtraction** (`DeckShapeReferenceGuide.md`), defines category ratios vs. `COMMANDER_TEMPLATE.md`, and sets target DTI tiers (`R1–S3`).
3. **Section 3 — Alternatives Considered & Rejected Tech:** Documents rejected sub-themes or cut traps and *why* they were rejected (preventing future sessions from re-adding them).
4. **Section 4 — Candidate 100-Card Pool / Swap Matrix Preview:** Lists the Scryfall-verified candidate pool (or runs `python scripts/swap_matrix.py ...` dry-run for overhauls).

---

### Workflow 3: `emm-review` (Zero-Context Minnow Audit Pipeline)

1. **Step 1 — Generate the Prose-Free Blind Spec (MANDATORY):**
   ```bash
   python scripts/minnow_prep.py "<deck_dir>" --pack
   ```
   *(For a proposed overhaul not yet applied, pass `--in ... --out ...` so the blind spec includes the raw delta without `--reason` strings.)*
2. **Step 2 — Dispatch the Zero-Context Minnow Swarm:**
   Launch parallel `research` subagents via `invoke_subagent` with `Mode: REVIEW` and target `<deck_dir>/minnow_blind_spec.txt` (NEVER pass the `.md` deck guide to `emm-comprehension`, `emm-zoom-out`, or `emm-design-critic`!).
   * **Minnow A (`emm-comprehension`):** Reads *only* `minnow_blind_spec.txt` and outputs its cold deduction of the deck's **3-Step Keystone**, **Geometric Shape**, **Target Bracket**, and any split-personality ambiguity.
   * **Minnow B (`emm-zoom-out` + `emm-design-critic`):** Reads `minnow_blind_spec.txt` and `DeckShapeReferenceGuide.md`, hunting for Commander Subtraction violations, Orphan Sub-Packages ($<6$ cards), mechanical nonbos (Shroud vs. Equipment, exile vs. dies, CR 302.6), Synergy Bricks when the Commander is taxed out, and pod interaction blind spots.
   * **Minnow C (`emm-codebase-details` + `emm-readiness`):** Audits statutory Bracket compliance (Game Changers, MLD), player preference bans (filter lands, filter Signets), `GOLDFISH_LOG.md`, `dti_eval.json`, and runs `python scripts/minnow_prep.py "<deck_dir>" --drift`.

---

### Workflow 4: `emm-resolve` (Elephant Arbitration & Interactive Resolution)

When the Minnow subagents return their raw critiques, the Elephant **does NOT blindly obey every complaint**. In the main session:

1. **Categorize Every Finding into 1 of 4 Strict Buckets:**
   * **`PROPOSE FIX`:** The Minnow caught a genuine mechanical nonbo, Deck Shape flaw, mana deficit, or preference violation. Formulate a concrete card swap or spec edit.
   * **`CONTEST`:** The Minnow critique is inaccurate or contradicted by checkable evidence (e.g., Scryfall oracle rules, DTI telemetry, or an explicit `Non-Goal`).
     * *Hard Rule:* **A contest must be checkable.** *"This was intentional"* is not evidence unless recorded in the deck's Non-Goals or supported by empirical Goldfish/DTI telemetry.
     * *Hard Rule:* **Never contest a Cold Comprehension gap.** If `emm-comprehension` could not deduce the deck's Keystone from the 100 cards, the card pool is objectively unfocused or diluted.
   * **`ESCALATE`:** The critique involves an unstated player preference, budget trade-off, or pet card decision. Surface `ESCALATE` items first to the user.
   * **`DECLINE`:** The finding is a minor **Nit**. Record it and do not bloat the deck to appease it (enforcing Dave Rensin's **2–3 round Nitpick Stopping Threshold**).

2. **Save `<deck_dir>/minnow_eval.json` and Render Reports:**
   Write the structured findings and Elephant resolutions to `<deck_dir>/minnow_eval.json` following this schema:
   ```json
   {
     "deck_name": "ObekaSplitterOfSeconds",
     "commander": "Obeka, Splitter of Seconds",
     "target_bracket": 3,
     "date": "2026-10-26",
     "status": "pending_resolution",
     "comprehension_check": {
       "cold_deduced_keystone": "Primary Action -> Capitalization -> Finisher deduced cold by Minnow",
       "intended_keystone": "Primary Action -> Capitalization -> Finisher intended by Elephant",
       "cold_deduced_shape": "Inverted Triangle / T-Shape (Commander = Amplifier)",
       "intended_shape": "Inverted Triangle / T-Shape (Commander = Amplifier)",
       "verdict": "PASS",
       "notes": "Diagnostic comparison notes..."
     },
     "findings": [
       {
         "title": "Short issue title",
         "lens": "emm-design-critic",
         "severity": "Blocker",
         "scope": "Equipment / Protection Suite",
         "cards": ["Whispersilk Cloak", "Ring of Valkas"],
         "description": "What the Minnow found cold...",
         "rationale": "Why this hurts the deck...",
         "elephant_resolution": "PROPOSE FIX",
         "elephant_justification": "Why the Elephant agrees, contests, or escalates...",
         "proposed_edit": "Swap Out: Whispersilk Cloak -> Swap In: Brotherhood Regalia"
       }
     ]
   }
   ```
   Then run:
   ```bash
   python scripts/minnow_prep.py "<deck_dir>" --render
   ```
   This generates `<deck_dir>/minnow_review_report.md` and `<deck_dir>/minnow_report.html`.

3. **Present the Interactive Resolution Gate:**
   Link [`minnow_report.html`](minnow_report.html) and [`minnow_review_report.md`](minnow_review_report.md) in chat, highlight any **`ESCALATE`** items first, and let the user choose:
   * **Auto accept:** Execute all `PROPOSE FIX` swaps via `python scripts/swap_matrix.py ...` (skipping `CONTEST` and `DECLINE`).
   * **Interactive breakdown:** Walk through each `PROPOSE FIX`, `CONTEST`, and `ESCALATE` item one-by-one.
   * **Continue without changes:** Lock the spec as-is.

---

### Workflow 5: `emm-drift-report` (Cross-File Consistency Audit)

Checks a single deck or the entire repository for divergence across `moxfield_import.txt`, the `.md` `Plain Text Copy/Paste` block (including the 2-trailing-space GFM rule), `Card Explanations` prose (catching ghost cards left behind after swaps), `dti_eval.json`, and MTG Forge `.dck` files:

```bash
# Single deck drift check:
python scripts/minnow_prep.py "<deck_dir>" --drift

# Repository-wide drift check across all Owned & Planning decks:
python scripts/minnow_prep.py --drift --all
```
