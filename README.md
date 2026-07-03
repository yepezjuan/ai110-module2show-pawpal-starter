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

## Features

- **Slot-aware sorting** — tasks are ordered by time of day (morning → midday → evening → anytime) before priority is considered, so the schedule reads naturally from start to finish.
- **Priority tie-breaking** — within the same slot, tasks are ranked high → medium → low; ties are broken by task-type criticality (medication is always first, then feed, walk, grooming, enrichment, other).
- **Conflict detection** — the greedy scheduler tracks two independent budgets: the owner's total daily minutes and each slot's capacity (morning 180 min, midday/evening 120 min each). Any task that busts either cap is moved to a "Not scheduled" conflict list with an explanatory reason string.
- **Conflict warnings in the UI** — each skipped task surfaces as a labeled `st.warning` in the Streamlit app so the owner knows exactly what was dropped and why.
- **Status filtering** — `filter_by_status()` separates completed from incomplete tasks; `generate_plan()` uses it to exclude already-done tasks before building today's schedule.
- **Per-pet filtering** — `filter_by_pet()` can isolate one pet's workload from a shared task list, useful when managing multiple pets.
- **Daily recurrence** — each `PetTask` carries a `recurring` flag (default `True`). Calling `Pet.reset_recurring_tasks()` clears `is_complete` only on recurring tasks, leaving one-off tasks permanently done so they never re-enter future plans.
- **Multi-pet scheduling** — `Scheduler` and `DailyPlan` both accept a list of `Pet` objects, so tasks from every pet compete for the same daily time budget and are grouped together in the output.

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

Run the full test suite with:

```bash
python -m pytest
```

The 7 tests cover the core scheduling behaviors:

- **Task completion** — `mark_complete()` flips `is_complete` from `False` to `True`
- **Adding tasks** — `pet.add_task()` grows the pet's task list
- **Sorting** — `sort_by_time_and_priority()` orders tasks by slot (morning → evening), then by priority and task-type criticality
- **Recurring tasks** — `reset_recurring_tasks()` clears `is_complete` on recurring tasks so they re-enter the next day's plan
- **Non-recurring tasks** — one-off tasks stay permanently complete after reset and are excluded from future plans
- **Slot overflow** — tasks that exceed a time-slot's capacity (e.g., morning cap of 180 min) are moved to the conflict list
- **Daily budget overflow** — tasks that exceed the owner's total daily minutes are flagged as conflicts

```
============================= test session starts ==============================
platform darwin -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/juanyepez/Documents/CP-AI-class/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 7 items

tests/test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.03s ===============================
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

### Streamlit UI features

The app is divided into two main areas:

**Task entry panel** — enter owner and pet details (name, species, breed, age), then use the four-column form to set a task title, type, duration, and priority. Click **Add task** to append it to the session. The task list below the form immediately re-sorts by slot and priority using `sort_by_time_and_priority()`, so you can see the scheduling order before generating a plan.

**Schedule panel** — set how many minutes are available today, then click **Generate schedule**. The app creates a `Pet`, attaches all entered tasks, builds a `Scheduler`, and calls `generate_plan()`. Results appear as:
- Three `st.metric` tiles: scheduled task count, total minutes, and conflict count.
- Tasks listed under bold slot headers (`MORNING`, `MIDDAY`, `EVENING`, `ANYTIME`).
- A yellow `st.warning` for each skipped task, showing the task name and the exact reason (e.g., *"exceeds daily time budget"* or *"morning slot full (180 min max)"*).

### Example workflow

1. Enter owner name `Jordan` and pet name `Mochi` (dog, Mixed, age 3).
2. Add a **Morning walk** — walk, 30 min, high priority.
3. Add a **Feeding** — feed, 10 min, high priority.
4. Add a **Grooming** — grooming, 45 min, low priority.
5. Notice the task list re-orders: Feeding and Morning walk (both morning, high) appear before Grooming (midday, low).
6. Set available minutes to **35** and click **Generate schedule**.
7. The metrics show **2 tasks, 40 min** — wait, 30 + 10 = 40, which fits. Grooming (45 min) lands in the conflict warning: *"Mochi: Grooming — exceeds daily time budget"*.
8. Increase available minutes to **90** and regenerate — all three tasks schedule cleanly, no warnings.

### Key Scheduler behaviors shown

| Behavior | Where you see it |
|---|---|
| Slot-aware sort | Task list preview re-orders as you add tasks |
| Priority tie-breaking | Within the same slot, high-priority tasks always appear first |
| Daily budget conflict | Yellow warning when total time exceeds the available minutes input |
| Slot capacity conflict | Yellow warning when a single slot's tasks exceed its cap (morning 180 min, midday/evening 120 min) |
| Status filtering | Already-completed tasks are excluded from `generate_plan()` automatically |
| Multi-pet support | Add a second pet and both pets' tasks compete for the same daily budget |

### CLI output (`python main.py`)

```
=============================================
  FILTER: Mochi's tasks only
=============================================
  ✓ Mochi: Grooming — 45 min [low] (midday)
  ○ Mochi: Morning walk — 30 min [high] (morning)
  ○ Mochi: Feeding — 10 min [high] (morning)

=============================================
  FILTER: incomplete tasks only
=============================================
  ○ Mochi: Morning walk — 30 min [high] (morning)
  ○ Mochi: Feeding — 10 min [high] (morning)
  ○ Luna: Playtime — 20 min [low] (evening)
  ○ Luna: Feeding — 10 min [medium] (morning)
  ○ Luna: Medication — 5 min [high] (morning)

=============================================
  FILTER: completed tasks only
=============================================
  ✓ Mochi: Grooming — 45 min [low] (midday)

=============================================
  SORTED: all tasks by slot + priority
=============================================
  ○ Luna: Medication — 5 min [high] (morning)
  ○ Mochi: Feeding — 10 min [high] (morning)
  ○ Mochi: Morning walk — 30 min [high] (morning)
  ○ Luna: Feeding — 10 min [medium] (morning)
  ✓ Mochi: Grooming — 45 min [low] (midday)
  ○ Luna: Playtime — 20 min [low] (evening)

=============================================
       TODAY'S SCHEDULE
=============================================
Daily plan for Mochi & Luna — 2026-07-02

  [MORNING]
    • ○ Luna: Medication — 5 min [high] (morning)
    • ○ Mochi: Feeding — 10 min [high] (morning)
    • ○ Mochi: Morning walk — 30 min [high] (morning)
    • ○ Luna: Feeding — 10 min [medium] (morning)

  [EVENING]
    • ○ Luna: Playtime — 20 min [low] (evening)

Total: 75 min

Summary: 5 tasks, 75 min total
=============================================
```

Mochi's Grooming task was marked complete before scheduling, so `filter_by_status()` excluded it — it appears in the completed filter but never enters the plan. All five remaining tasks fit within the 90-minute daily budget, so no conflicts are raised.
