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
=============================================
           TODAY'S SCHEDULE
=============================================

Daily plan for Mochi & Luna — 2026-07-01
  • Mochi: Morning walk — 30 min [high]
  • Mochi: Feeding — 10 min [high]
  • Luna: Medication — 5 min [high]
  • Luna: Feeding — 10 min [medium]
  • Luna: Playtime — 20 min [low]
Total: 75 min

Summary: 5 tasks, 75 min total
=============================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature           | Method(s) | Notes |
| ----------------- | --------- | ----- |
| Task sorting | `Scheduler.sort_by_time_and_priority()` | Primary sort by time slot (morning → midday → evening → anytime), then descending priority (high → medium → low), then task-type criticality (medication before feed, walk, grooming, enrichment, other). A simpler `Scheduler.sort_by_priority()` is also available for priority-only ordering. |
| Filtering by pet | `Scheduler.filter_by_pet(tasks, pet_name)` | Returns only tasks whose `pet_name` matches the given string; useful for showing a single pet's workload. |
| Filtering by status | `Scheduler.filter_by_status(tasks, completed)` | Returns tasks matching the given completion state (`False` = incomplete, `True` = done). `generate_plan()` calls this to exclude already-completed tasks before building the schedule. |
| Conflict detection | `Scheduler.filter_by_time(tasks)` | Greedy scheduler that tracks two budgets: the owner's total daily minutes (`available_minutes_per_day`) and per-slot capacities (morning 180 min, midday/evening 120 min each). Any task that would exceed either cap is moved to the conflict list with an explanatory reason string and surfaced in `DailyPlan.display()` under "Not scheduled". |
| Recurring tasks | `PetTask.recurring`, `PetTask.reset()`, `Pet.reset_recurring_tasks()` | Each `PetTask` carries a `recurring` boolean (defaults to `True`). Calling `PetTask.reset()` clears `is_complete` only when `recurring` is `True`, leaving one-off tasks permanently done. `Pet.reset_recurring_tasks()` iterates all tasks and calls `reset()` on each, preparing the pet's roster for the next day's plan. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
