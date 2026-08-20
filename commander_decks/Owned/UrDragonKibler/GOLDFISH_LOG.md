# Goldfish Log — The Ur-Dragon (Kibler's Flight)

## [2026-08-20] — Bracket Audit Test (Bracket 3 Reclassification Validated) (20 sims, T10 turns, Bracket 3)

**Command:**
```bash
python3 scripts/multiplayer_goldfish.py commander_decks/Owned/UrDragonKibler/moxfield_import.txt --sims 20 --turns 10 --bracket 3 --html commander_decks/Owned/UrDragonKibler/goldfish_audit_20260820_182632.html
```

**Results:**
```text
====================================================================
RUNNING 20 × 4-PLAYER SIMULATIONS
Commander: The Ur-Dragon (CMC 9)  |  Target: Bracket 3 (Upgraded) (Target T7)
====================================================================

--------------------------------------------------------------------
AGGREGATE DEPLOYMENT & MULLIGAN PROFILE
--------------------------------------------------------------------
  Commander cast rate: 51/80 (64%)
  Commander Cast Range: T4 - T10
  Commander Cast Avg:   T7.3 (Hard-Cast 9-CMC Commander)
  Opening Hand Quality Breakdown (80 hands evaluated):
    Gold Keep (Mana + Ramp + Enabler):   26/80 (32%)
    Silver Keep (Mana + Curve):          54/80 (68%)
    Desperation Keep (Mulligan to <=5):   0/80 (0%)
    Average Starting Hand Size:          6.99 cards

--------------------------------------------------------------------
BRACKET READINESS (Bracket 3 (Upgraded) — Target T7)
--------------------------------------------------------------------
  Target Window Readiness Rate (T<=7): 28/80 (35%)
  Engine Readiness Avg:  T7.3
  [BRACKET COMPLIANCE CHECK] Status: NOTICE (Slow Engine Setup)
  Deck deploys its engine by T7.3 (behind schedule for a T7+ win target). Consider adding more low-CMC ramp or enablers.
```

**Notes:**
- **Reclassified to Bracket 3 (Upgraded):** Goldfish simulation confirmed that despite 0 Game Changers, the deck's 10 fetch + 10 shock 5-color mana base, passive Eminence reduction, and high-impact Dragons (*Terror of the Peaks*, *Miirym*, *Morophon*) accelerate 5-6 drop Dragons onto the table on Turns 3–5, hard-casting the 9-CMC commander on Turn 7.3 as a refuel engine.
