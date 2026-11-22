# AI Companion Integration Roadmap

> **Purpose:** A staged, low-risk plan for evolving the MTG Deck Collection AI companion using proven patterns from three open-source Commander projects:
> - [`nathanmartins/mtg-mcp`](https://github.com/nathanmartins/mtg-mcp) (Go MCP Server)
> - [`andreasvig/MTG-agentic-deck-builder`](https://github.com/andreasvig/MTG-agentic-deck-builder) (MAGE)
> - [`KoalaTrapLord/commander-ai-lab`](https://github.com/KoalaTrapLord/commander-ai-lab) (Commander AI Lab)
>
> **Strategy:** Implement **Phase 1 (`mtg-mcp`)** first for immediate data, meta, and validation value with zero disruption to existing scripts. Keep **Phases 2–5** documented in the backlog to pull in only when a concrete workflow bottleneck justifies them.

---

## Roadmap Overview

| Phase | Source Repo | Focus | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | `nathanmartins/mtg-mcp` | MCP Data, EDHREC, External Decks & Rules Validation | **Active — Next Up** |
| **Phase 2** | `commander-ai-lab` | ForgeSim Telemetry Post-Processing (`Sim Insights` Flags) | Backlog (Evaluate Later) |
| **Phase 3** | `commander-ai-lab` | Structured Precon & Anti-Synergy Audit Rubric | Backlog (Evaluate Later) |
| **Phase 4** | `MAGE` | Iterative Edit Loop, `--undo`, Compact Inspect & Deck Brief | Backlog (Evaluate Later) |
| **Phase 5** | `MAGE` + `commander-ai-lab` | Local Semantic Card Search + `collection.csv` Substitution | Backlog (Evaluate Later) |

---

## Phase 1: `mtg-mcp` Data & Validation Layer (Active — Next Up)

### Why First
`mtg-mcp` is an external MCP server that plugs directly into the AI client without modifying our existing Python toolchain (`scripts/swap_matrix.py`, `scripts/manapool_price_deck.py`, `scripts/dti_evaluator.py`, `forgesim_cluster/`). It immediately fills our biggest data gaps: **EDHREC synergy/combo data**, **direct Moxfield/Archidekt deck fetching**, and **Comprehensive Rules lookup**.

### Capabilities Gained
* **EDHREC Meta Data:** `get_edhrec_recommendations` (supports `theme` slugs and `price_tier`: `budget`/`expensive`, synergy scores, inclusion rates, salt scores), `get_edhrec_combos` (combo prerequisites and results by color identity), and `get_edhrec_set_cards`.
* **External Deck Ingestion:** `get_moxfield_deck`, `search_moxfield_decks`, `get_archidekt_deck` (including `lands_only: true` for token-efficient landbase comparisons), and `search_archidekt_decks` (with `bracket` filter 1–4).
* **Batched 100-Card Validation:** `validate_deck` checks Rule 903.3 commander eligibility (including Vehicles, Spacecraft with P/T, and *"can be your commander"* text), singleton exemptions (*"any number of"* / *"up to N"*), color identity, and the live ban list using Scryfall `/cards/collection` in batches of 75 (2 requests per deck).
* **Comprehensive Rules:** `get_rule`, `search_rules`, and `get_glossary_term` backed by WotC's official Comprehensive Rules text.

### Tool Boundary Rules (Keep Existing Strengths)
* **Keep `scripts/manapool_price_deck.py`** for live Manapool vendor pricing and stock checks (`mtg-mcp` only provides Scryfall USD/EUR/BRL).
* **Keep `scripts/scryfall_lookup.py`** for repo-shared `cache/scryfall_cards.json` lookups and verified image/Scryfall URI formatting in Markdown & HTML reports.
* **Keep `scripts/swap_matrix.py`** for all deck edits, Triple-Update synchronization, Rules Watchdog checks, and Forge `.dck` export.

### Implementation Checklist
- [ ] **1.1 Install Go & Build `mtg-mcp.exe`:** Install Go (`winget install GoLang.Go`, `1.27.3+`), clone `nathanmartins/mtg-mcp` to `C:\Antigravity\mtg-mcp` (keeping all AI projects under `C:\Antigravity`), and run `go build -o mtg-mcp.exe ./cmd/mtg-mcp`.
- [ ] **1.2 Register MCP Server:** Add `mtg-commander` to Antigravity's MCP configuration pointing to `C:\\Antigravity\\mtg-mcp\\mtg-mcp.exe`.
- [ ] **1.3 Update Working Documentation & Instructions:**
  - **`GEMINI.md`:** Update Sections 3 (`Repository Map`), 4 (`Session Startup Checklist`), 5.1 (`Card Verification`), 5.3–5.4 (`100-Card Singleton` & `Bracket Compliance`), and 12 (`Mandatory Agentic Workflows`) so every session knows `mtg-commander` is available and when to call it.
  - **`API_REFERENCE.md`:** Add an **"MCP Server (`mtg-commander`)"** section defining the tool-routing matrix alongside `scripts/scryfall_lookup.py`, `scripts/manapool_price_deck.py`, and `scripts/swap_matrix.py`.
- [ ] **1.4 Smoke Test (`ValgavothEndlessPunishment`):** Run `validate_deck` on `commander_decks/Owned/ValgavothEndlessPunishment/moxfield_import.txt`, `get_edhrec_recommendations` for **Valgavoth, Harrower of Souls**, a reference deck lookup (`get_moxfield_deck` / `get_archidekt_deck`), and `get_rule` (e.g., `302.6` / `903.3`).

---

## Phase 2: Telemetry-Driven Coaching (`Sim Insights`) — Backlog

* **Source:** `KoalaTrapLord/commander-ai-lab` (`coach/prompt_template.py`)
* **When to Pull In:** When reviewing 100-game `forgesim_cluster/` pod gauntlets feels too manual and we want automated, card-level cut candidates surfaced directly from simulation logs.
* **What to Adopt:**
  * Add a Python post-processor for `ForgePodRunner.java` / `scripts/forge_pod_sim.py` Seat 1 telemetry (which already records rejected mulligans, kept hands, draws, and turn-by-turn casts).
  * Compute per-card `keptInOpeningHandRate`, `avgTurnCast`, and `deadCardRate`.
  * Emit inline diagnostic flags in `FORGE_POD_LOG.md`:
    * `[OPENING HAND TRAP]` — `keptInOpeningHandRate < 0.25` (or below deck average)
    * `[LATE CASTER]` — `avgTurnCast > 6`
    * `[ISOLATED]` — low co-occurrence / synergy with the deck's core plan

---

## Phase 3: Structured Precon & Anti-Synergy Audit Rubric — Backlog

* **Source:** `KoalaTrapLord/commander-ai-lab` (`coach/prompt_template.py`)
* **When to Pull In:** When we want standardized, machine-checkable critique sections across all precon baselines and `.agents/skills/dti-auditor` / `.agents/skills/elephant-minnow` reviews.
* **What to Adopt:**
  * `removalCoverage`: Breakdown by permanent type (`creatures`, `artifacts`, `enchantments`, `planeswalkers`, `lands`, `massRemoval`) + explicit `gaps`.
  * `rampQuality`: Separate `manaRocks`, `landFetch`, `manaDorks`, `costReducers`, score `fragility`, and evaluate `canReachFourByTurnThree`.
  * `drawEngineProfile`: Separate `burstDraw` (one-time) from `repeatableEngines` + `sustainability`.
  * `antiSynergyFlags`: Explicit `{cards, conflict, severity}` list for nonbos.
  * `commanderDependency`: `score` (1–10), `dependentCards`, and `recoveryPlan`.

---

## Phase 4: Iterative Edit Loop, `--undo` & Deck Brief — Backlog

* **Source:** `andreasvig/MTG-agentic-deck-builder` (MAGE — `config.yaml`, `deck_agent_tools.py`, `deck_agent.py`)
* **When to Pull In:** When rapid, multi-turn conversational deck tuning makes rolling back swaps or preserving player constraints across sessions cumbersome.
* **What to Adopt:**
  * **Atomic Undo (`--undo`):** Extend `scripts/swap_matrix.py` to roll back the last Triple-Update transaction and record `(undone)` markers so the assistant does not re-suggest reverted cuts.
  * **Compact Deck Inspection (`--inspect`):** Add a token-light deck summary mode (`mana` curve / `price` totals by type, without full oracle text) modeled on MAGE's `read_deck(extra_info)`.
  * **Living Deck Brief:** Add a concise, overwritten "Deck Brief" block at the top of `DECK_TEMPLATE.md` capturing durable intent (target bracket, exclusions, pilot complexity, budget) rather than an append-only diary.
  * **Web-to-Catalog Gate:** Enforce that any card name discovered via web search or external primers is verified via `mtg-mcp` / `scryfall_lookup.py` before being proposed.

---

## Phase 5: Local Semantic Card Search & Collection Substitution — Backlog

* **Source:** `MAGE` (`semantic_index.py`, `agentic_card_search.py`) + `commander-ai-lab` (`coach/services/deck_generator.py`)
* **When to Pull In:** When Scryfall query syntax + EDHREC recommendations are insufficient for nuanced natural-language queries (e.g., *"repeatable ways to untap artifacts under \$2"*), or when auto-substituting new brews against owned inventory.
* **What to Adopt:**
  * **Local Semantic + Filter Index:** Upgrade `scripts/scryfall_recommend.py` with a local SQLite + `FastEmbed` (`BAAI/bge-small-en-v1.5`) index over Scryfall bulk data and Tagger tags, preserving MAGE's temporary-ID selection (`R001`, `R002`, ...) and *"you own your filters"* design.
  * **Non-Destructive `smart_substitute`:** Adopt `commander-ai-lab`'s 5-step fallback (`EXACT_MATCH` → `FUZZY_MATCH` → `EMBEDDING_ANALOG` → `ORIGINAL_KEPT` → `BASIC_LAND_FALLBACK`) against `collection.csv`, paired with a hard `sum(SLOT_BUDGET) == 99` assertion.
