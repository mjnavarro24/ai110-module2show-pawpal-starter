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
collected 22 items                                                                                 

tests/test_pawpal.py ......................                                                  [100%]

=============== 22 passed in 0.02s ==================```
```

python -m pytest tests/test_pawpal.py

### What the tests cover

The suite in `tests/test_pawpal.py` exercises the core scheduling behaviors:

- **Task & pet basics** — marking a task complete flips its status, and adding a task increases the pet's task count.
- **Conflict detection** — overlapping tasks are flagged, tasks with identical start times conflict, and three mutually overlapping tasks report all pairs. Back-to-back tasks (one ending as the next starts) and zero-duration tasks are correctly treated as *non*-conflicts. A dedicated test confirms the early-exit optimization in `find_conflicts` still catches a later overlap hidden behind a non-overlapping gap.
- **Sorting** — `sort_by_time` returns a day's tasks in chronological order and excludes tasks from other days.
- **Filtering** — `filter_tasks` narrows by completion status, by pet name, and returns everything when no filters are given.
- **Recurring tasks** — completing a one-off task spawns nothing; a daily task spawns a pending copy one day later and a weekly task seven days later. Completion is idempotent, so re-completing never creates duplicate occurrences.
- **Schedule generation** — `generate_schedule` surfaces conflicts and notes them in the plan's explanation.
- **Multiple pets** — `all_tasks` and `pending_tasks` aggregate across every pet an owner has, `find_conflicts` flags an overlap between two *different* pets' tasks, and `generate_schedule` orders tasks drawn from multiple pets by priority then time.

Confidence Level: 5

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Schedule generation | `generate_schedule` | Orders pending tasks by priority (HIGH → LOW), tie-broken by start time; returns a `Plan`. Spans every pet the owner has. |
| Task sorting | `sort_by_time` | Returns a single day's tasks in chronological order; excludes tasks from other days. |
| Filtering | `filter_tasks`, `pending_tasks` | Narrows by completion status and/or pet name; returns all tasks when no filter is given. |
| Conflict handling | `find_conflicts`, `Task.overlaps` | Flags overlapping time intervals using half-open ranges (back-to-back and zero-duration tasks don't conflict); catches conflicts *across different pets*; sort-and-early-exit scan. |
| Recurring tasks | `complete_task`, `Task.next_occurrence` | Completing a task spawns the next occurrence one day (daily) or seven days (weekly) later; idempotent, so no duplicates. |
| Multiple pets | `Owner.all_tasks`, `Owner.pets` | An owner can hold many pets; task aggregation, filtering, sorting, and scheduling all operate across the full set. |
| Explainable plans | `generate_schedule` | Each `Plan` carries an `explanation` (task count, total minutes, ordering, conflict count). |

## 📸 Demo Walkthrough

### What the UI lets you do

The Streamlit app (`app.py`) is organized top-to-bottom around one owner and any number of their pets:

- **Owner info** — enter the owner's name.
- **Add pets** — register one or more pets by name and age; duplicate names are rejected, and the current roster is shown beneath the form.
- **Add tasks** — pick which pet the task is for, then give it a title, duration (minutes), priority (low/medium/high), and frequency (none/daily/weekly), and click **Add task**.
- **Browse & filter tasks** — view all current tasks in a table (with a **Pet** column) and filter them by status (All/Pending/Completed) and by pet.
- **Mark a task complete** — pick a pending task and complete it; recurring tasks automatically spawn their next occurrence, and the app tells you when it's scheduled.
- **Remove a task** — delete any task from its pet.
- **Today's Timeline** — see all of today's tasks, across every pet, ordered by time of day (each row labeled with its pet).
- **Build Schedule** — click **Generate schedule** to produce a prioritized daily plan spanning all pets, read its plain-language explanation, and see any time conflicts (including cross-pet ones) called out in a warning table.

### Example workflow

1. Enter the owner (e.g., *Jordan*).
2. Add two pets — *Mochi* and *Rex*.
3. Add a task for Mochi — *Morning walk*, 20 min, high priority, daily.
4. Add a task for Rex — *Vet visit*, 60 min, medium priority — at an overlapping time.
5. Watch the **Today's Timeline** table interleave both pets' tasks chronologically, each tagged with its pet.
6. Click **Generate schedule** to get a priority-ordered plan spanning both pets, with an explanation.
7. Review the ⚠️ conflict table if the two pets' tasks overlap.
8. Mark the daily walk complete and confirm the next day's occurrence appears.

### Key Scheduler behaviors on display

- **Sorting by time** — `Today's Timeline` uses `sort_by_time` to show a day's tasks chronologically across all pets.
- **Priority ordering** — `generate_schedule` orders the plan by priority (HIGH → LOW), tie-broken by start time.
- **Conflict warnings** — overlapping tasks are surfaced via `find_conflicts` and flagged in the plan, including conflicts between two different pets.
- **Daily/weekly recurrence** — completing a recurring task spawns its next occurrence automatically.
- **Filtering** — tasks can be narrowed by completion status and by pet via `filter_tasks`.
- **Multiple pets** — every table and the generated schedule aggregate tasks across all of an owner's pets, each row labeled with the pet it belongs to.

### Sample CLI output

Running the demo script reproduces these behaviors in the terminal:

```bash
python main.py
```

```
Today's Schedule
========================================
Alex — Sunday, July 05, 2026

07:00 AM  [MEDIUM] Breakfast (Whiskers) — 10 min
08:00 AM  [HIGH  ] Morning walk (Rex) — 30 min
03:00 PM  [MEDIUM] Vet appointment (Rex) — 60 min
06:30 PM  [HIGH  ] Feed Whiskers (Whiskers) — 10 min

Completing Whiskers' daily Breakfast...
----------------------------------------
Auto-created next occurrence for Monday, July 06: 07:00 AM  [MEDIUM] Breakfast (Whiskers) — 10 min

Pending tasks
----------------------------------------
03:00 PM  [MEDIUM] Vet appointment (Rex) — 60 min
08:00 AM  [HIGH  ] Morning walk (Rex) — 30 min
06:30 PM  [HIGH  ] Feed Whiskers (Whiskers) — 10 min
07:00 AM  [MEDIUM] Breakfast (Whiskers) — 10 min

Completed tasks
----------------------------------------
07:00 AM  [MEDIUM] Breakfast (Whiskers) — 10 min

Rex's tasks
----------------------------------------
03:00 PM  [MEDIUM] Vet appointment (Rex) — 60 min
08:00 AM  [HIGH  ] Morning walk (Rex) — 30 min
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
