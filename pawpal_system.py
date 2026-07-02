from dataclasses import dataclass, field
from datetime import date


# Higher number = higher priority, used for ascending sort
PRIORITY_ORDER = {"low": 0, "medium": 1, "high": 2}

# Lower number = more critical type, used for ascending sort within same priority
TYPE_ORDER = {"medication": 0, "feed": 1, "walk": 2, "grooming": 3, "enrichment": 4, "other": 5}

SLOT_ORDER = {"morning": 0, "midday": 1, "evening": 2, "anytime": 3}

_NO_SLOT_CAP = float("inf")  # sentinel: slot has no upper time limit

# Max minutes the owner realistically has in each part of the day
SLOT_CAPACITY = {"morning": 180, "midday": 120, "evening": 120, "anytime": _NO_SLOT_CAP}

# Sensible default slot for each task type so owners don't have to set it manually
DEFAULT_SLOT = {
    "feed":        "morning",
    "medication":  "morning",
    "walk":        "morning",
    "grooming":    "midday",
    "enrichment":  "evening",
    "other":       "anytime",
}


@dataclass
class PetTask:
    """Represents a single care task with priority, time slot, and recurrence."""

    title: str
    task_type: str           # "walk", "feed", "medication", "grooming", "enrichment", "other"
    duration_minutes: int
    priority: str            # "low", "medium", "high"
    pet_name: str = ""       # stamped automatically when added to a Pet
    is_complete: bool = False
    recurring: bool = True   # if True, reset() re-enables it for the next day's plan
    time_slot: str = ""      # "morning", "midday", "evening", "anytime" — inferred if blank

    def __post_init__(self) -> None:
        if not self.time_slot:
            self.time_slot = DEFAULT_SLOT.get(self.task_type, "anytime")

    def mark_complete(self) -> None:
        """Mark this task done; recurring tasks can be reset to repeat the next day."""
        self.is_complete = True

    def reset(self) -> None:
        """Clear completion state so a recurring task re-enters tomorrow's schedule."""
        if self.recurring:
            self.is_complete = False

    def get_summary(self) -> str:
        """One-line label: completion status, pet, title, duration, priority, slot."""
        status = "✓" if self.is_complete else "○"
        return (
            f"{status} {self.pet_name}: {self.title} — "
            f"{self.duration_minutes} min [{self.priority}] ({self.time_slot})"
        )


@dataclass
class Pet:
    """Represents a pet and owns the list of care tasks associated with it."""

    name: str
    species: str
    breed: str
    age: int
    tasks: list[PetTask] = field(default_factory=list)

    def add_task(self, task: PetTask) -> None:
        """Attach a task to this pet, stamping it with the pet's name before storing."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: PetTask) -> None:
        """Remove an existing task by reference."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[PetTask]:
        """Return a shallow copy of this pet's task list to prevent external mutation."""
        return list(self.tasks)

    def reset_recurring_tasks(self) -> None:
        """Clear completion on all recurring tasks to prepare for a new day's plan."""
        for task in self.tasks:
            task.reset()


class Scheduler:
    """Builds a DailyPlan by sorting, filtering, and conflict-checking all pet tasks."""

    def __init__(self, pets: list[Pet], available_minutes_per_day: int) -> None:
        """Store the pet roster and the daily time cap used by generate_plan."""
        self.pets = pets
        self.available_minutes_per_day = available_minutes_per_day

    def generate_plan(self) -> "DailyPlan":
        """Collect eligible tasks, sort by slot+priority, fit within budget, detect conflicts."""
        all_tasks: list[PetTask] = []
        for pet in self.pets:
            all_tasks.extend(self.filter_by_status(pet.get_tasks(), completed=False))

        sorted_tasks = self.sort_by_time_and_priority(all_tasks)
        fitting_tasks, conflicts = self.filter_by_time(sorted_tasks)

        plan = DailyPlan(pets=self.pets, date=date.today().isoformat())
        for task in fitting_tasks:
            plan.add_task(task)
        for task, reason in conflicts:
            plan.add_conflict(task, reason)
        return plan

    # ------------------------------------------------------------------ filtering

    def filter_by_pet(self, tasks: list[PetTask], pet_name: str) -> list[PetTask]:
        """Return only tasks belonging to the named pet."""
        return [t for t in tasks if t.pet_name == pet_name]

    def filter_by_status(
        self, tasks: list[PetTask], completed: bool = False
    ) -> list[PetTask]:
        """Return tasks matching the given completion state (False=incomplete, True=done)."""
        return [t for t in tasks if t.is_complete == completed]

    # ------------------------------------------------------------------ sorting

    def sort_by_time_and_priority(self, tasks: list[PetTask]) -> list[PetTask]:
        """Sort by time slot, then descending priority, then task-type criticality."""
        return sorted(
            tasks,
            key=lambda t: (
                SLOT_ORDER.get(t.time_slot, 3),     # morning first
                -PRIORITY_ORDER.get(t.priority, 0), # high before low
                TYPE_ORDER.get(t.task_type, 5),     # medication before feed, etc.
            ),
        )

    def sort_by_priority(self, tasks: list[PetTask]) -> list[PetTask]:
        """Sort by priority only (highest first). Kept for backward compatibility."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority], reverse=True)

    # ------------------------------------------------------------------ time budget

    def filter_by_time(
        self, tasks: list[PetTask]
    ) -> tuple[list[PetTask], list[tuple[PetTask, str]]]:
        """Greedily schedule tasks; flag any that bust the daily budget or slot capacity.

        Returns (scheduled_tasks, [(conflict_task, reason), ...]).
        """
        result: list[PetTask] = []
        conflicts: list[tuple[PetTask, str]] = []
        remaining = self.available_minutes_per_day
        slot_used: dict[str, int] = {s: 0 for s in SLOT_CAPACITY}

        for task in tasks:
            slot = task.time_slot
            cap = SLOT_CAPACITY.get(slot, 9999)
            used = slot_used.get(slot, 0)

            if task.duration_minutes > remaining:
                conflicts.append((task, "exceeds daily time budget"))
            elif used + task.duration_minutes > cap:
                conflicts.append((task, f"{slot} slot full ({cap} min max)"))
            else:
                result.append(task)
                remaining -= task.duration_minutes
                slot_used[slot] = used + task.duration_minutes

        return result, conflicts


class DailyPlan:
    """Holds the final scheduled task list and any conflicts flagged during planning."""

    def __init__(self, pets: list[Pet], date: str) -> None:
        """Initialize an empty plan for the given pets and ISO date string."""
        self.pets = pets
        self.date = date
        self.scheduled_tasks: list[PetTask] = []
        self.conflicts: list[tuple[PetTask, str]] = []
        self.total_duration_minutes: int = 0

    def add_task(self, task: PetTask) -> None:
        """Append a task to the schedule and accumulate its duration."""
        self.scheduled_tasks.append(task)
        self.total_duration_minutes += task.duration_minutes

    def add_conflict(self, task: PetTask, reason: str) -> None:
        """Record a task that couldn't be scheduled and the reason why."""
        self.conflicts.append((task, reason))

    def display(self) -> str:
        """Format the full plan as a human-readable string grouped by time slot."""
        pet_names = " & ".join(p.name for p in self.pets)
        lines = [f"Daily plan for {pet_names} — {self.date}"]

        current_slot: str | None = None
        for task in self.scheduled_tasks:
            if task.time_slot != current_slot:
                current_slot = task.time_slot
                lines.append(f"\n  [{current_slot.upper()}]")
            lines.append(f"    • {task.get_summary()}")

        lines.append(f"\nTotal: {self.total_duration_minutes} min")

        if self.conflicts:
            lines.append("\nNot scheduled:")
            for task, reason in self.conflicts:
                lines.append(f"  ✗ {task.get_summary()} — {reason}")

        return "\n".join(lines)

    def get_summary(self) -> str:
        """One-line overview: task count, total time, and conflict count if any."""
        conflict_note = f", {len(self.conflicts)} conflict(s)" if self.conflicts else ""
        return f"{len(self.scheduled_tasks)} tasks, {self.total_duration_minutes} min total{conflict_note}"
