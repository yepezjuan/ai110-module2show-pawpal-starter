# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- there is only one user for this version where, the user can have multiple pets, each pet can then have multiple tasks. where each task is categorized and given a priority order which is then used to make a task schedule for the user

- What classes did you include, and what responsibilities did you assign to each?

  Pet Class:
  Pet Task Class:
  Task Schedule Class
  Task Class

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, it did change I removed 2 functions from init design:

ScheduledTask The indirection of wrapping a PetTask with time slots is not needed yet. DailyPlan will hold an ordered list of PetTask objects directly; time display can be computed on-the-fly when rendering.
Frequency (enum) Recurring task frequency adds complexity to is_due_today() without a task history mechanism to back it. Removed entirely for v1; PetTask.is_recurring can stay as a bool if needed, but the Frequency enum is dropped.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- it can only have one user for right now
- Why is that tradeoff reasonable for this scenario?
- want to only make a working MVP, can extend to mulit owner later:

The scheduler prioritizes predictability over optimality — an owner always knows their highest-priority tasks are scheduled first, but the greedy approach can waste available time by letting one large task block several smaller ones that together would have fit.

## for the mvp I only had one owner so i didnt make a owner class. that would be for later development

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

it took some play in all off the process, i did most of the design work brainstorming all the classes that i thought would fit into the project and narrowing it down to the most essential in order to get a MVP. while still maintaining ideas for later improvements

- What kinds of prompts or questions were most helpful?

An important one was, optimizing the scheduling algorithm. how can it be optimized so that its not scheduling just based off priority. Also had to redo the the scheduler so that it would take in multiple pets to make ONE schedule, not have one schedule PER pet.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

In early prompts the agent wanted to develop a Owner class, however I did not want to add that complexity to the project.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

  - `mark_complete()` changes `is_complete` from False to True — verifies the most basic state transition in a task's lifecycle.
  - Adding a task to a `Pet` increases `pet.tasks` count — confirms `add_task()` correctly stores tasks.
  - `sort_by_time_and_priority()` orders tasks by slot first (morning before evening), then by descending priority, then by task-type criticality (medication before feed) — validates the core scheduling ordering logic.
  - Recurring tasks reappear in the plan after `reset_recurring_tasks()` is called — ensures the daily-reset workflow works end to end.
  - Non-recurring tasks stay complete after a reset and are excluded from the generated plan — guards against one-time tasks accidentally repeating.
  - A task that overflows a slot's time cap (e.g. morning is capped at 180 min) is moved to conflicts with the correct reason string — verifies slot-capacity enforcement.
  - A task whose duration exceeds the owner's available daily minutes is flagged as a conflict — verifies the global time-budget guard.

- Why were these tests important?

  The scheduler's correctness depends on three guarantees working together: tasks sort in the right order, time constraints are enforced at both the slot and daily level, and completion state resets cleanly for recurring tasks. Testing each of these independently made it easy to isolate exactly which guarantee broke when I changed the sorting key or conflict logic.

**b. Confidence**

- How confident are you that your scheduler works correctly?

  I'm fairly confident in the happy path and the two main conflict cases (slot overflow and daily budget overflow). The tests cover the exact constraints the scheduler enforces, so if those fail I'd know immediately. I'm less confident about multi-pet edge cases — the tests use single-pet setups almost exclusively, so subtle bugs in how tasks from different pets interleave in the sorted order could still exist.

- What edge cases would you test next if you had more time?

  - Two pets each with tasks that together exactly fill the daily budget — verify no off-by-one causes a false conflict.
  - A task with an unknown `task_type` (e.g. `"swim"`) to confirm `DEFAULT_SLOT` and `TYPE_ORDER` fall back gracefully to `"anytime"` and the lowest sort position.
  - All tasks already complete before `generate_plan()` is called — the resulting plan should be empty with no conflicts.
  - A mix of recurring and non-recurring tasks across the reset cycle to confirm only the right subset comes back.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
