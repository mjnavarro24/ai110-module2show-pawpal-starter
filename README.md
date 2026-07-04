# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Today's Schedule
========================================
Alex — Wednesday, July 01, 2026

08:00 AM  [HIGH  ] Morning walk (Rex) — 30 min
03:00 PM  [MEDIUM] Vet appointment (Rex) — 60 min
06:30 PM  [HIGH  ] Feed Whiskers (Whiskers) — 10 min

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
python3 -m pytest
======================================= test session starts ========================================
platform darwin -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/melaynanavarro/codepath/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 18 items                                                                                 

tests/test_pawpal.py ..................                                                      [100%]

=============== 18 passed in 0.01s ==================```

python -m pytest tests/test_pawpal.py

### What the tests cover

The suite in `tests/test_pawpal.py` exercises the core scheduling behaviors:

- **Task & pet basics** — marking a task complete flips its status, and adding a task increases the pet's task count.
- **Conflict detection** — overlapping tasks are flagged, tasks with identical start times conflict, and three mutually overlapping tasks report all pairs. Back-to-back tasks (one ending as the next starts) and zero-duration tasks are correctly treated as *non*-conflicts. A dedicated test confirms the early-exit optimization in `find_conflicts` still catches a later overlap hidden behind a non-overlapping gap.
- **Sorting** — `sort_by_time` returns a day's tasks in chronological order and excludes tasks from other days.
- **Filtering** — `filter_tasks` narrows by completion status, by pet name, and returns everything when no filters are given.
- **Recurring tasks** — completing a one-off task spawns nothing; a daily task spawns a pending copy one day later and a weekly task seven days later. Completion is idempotent, so re-completing never creates duplicate occurrences.
- **Schedule generation** — `generate_schedule` surfaces conflicts and notes them in the plan's explanation.

Confidence Level: 5

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | sort_by_time | e.g., by priority, duration |
| Filtering | filter_tasks | e.g., skip tasks if time runs out |
| Conflict handling |find_conflicts | e.g., overlapping time slots |
| Recurring tasks | complete_task | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
