from dataclasses import dataclass, field
from datetime import date


@dataclass
class PetTask:
    """Represents a single care task assigned to a pet, with priority and completion state."""

    title: str
    task_type: str          # "walk", "feed", "medication", "grooming", "enrichment", "other"
    duration_minutes: int
    priority: str           # "low", "medium", "high"
    pet_name: str = ""      # set automatically when added to a Pet
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done so it can be filtered out of future scheduling passes."""
        self.is_complete = True

    def get_summary(self) -> str:
        """Return a single-line label combining pet name, title, duration, and priority."""
        return f"{self.pet_name}: {self.title} — {self.duration_minutes} min [{self.priority}]"


@dataclass
class Pet:
    """Represents a pet and owns the list of care tasks associated with it."""

    name: str
    species: str
    breed: str
    age: int
    tasks: list[PetTask] = field(default_factory=list)

    def add_task(self, task: PetTask) -> None:
        """Attach a task to this pet, stamping it with the pet's name before storing it."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: PetTask) -> None:
        """Remove an existing task from this pet's task list by reference."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[PetTask]:
        """Return a shallow copy of this pet's task list to prevent external mutation."""
        return list(self.tasks)


PRIORITY_ORDER = {"low": 0, "medium": 1, "high": 2}


class Scheduler:
    """Builds a DailyPlan by sorting all pet tasks by priority and fitting them within a time budget."""

    def __init__(self, pets: list[Pet], available_minutes_per_day: int):
        """Store the pet roster and the daily time cap used by generate_plan."""
        self.pets = pets
        self.available_minutes_per_day = available_minutes_per_day

    def generate_plan(self) -> "DailyPlan":
        """Collect, sort, and time-filter all tasks across pets into a single DailyPlan."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        sorted_tasks = self.sort_by_priority(all_tasks)
        fitting_tasks = self.filter_by_time(sorted_tasks)
        plan = DailyPlan(pets=self.pets, date=date.today().isoformat())
        for task in fitting_tasks:
            plan.add_task(task)
        return plan

    def sort_by_priority(self, tasks: list[PetTask]) -> list[PetTask]:
        """Return tasks ordered from highest to lowest priority using PRIORITY_ORDER weights."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority], reverse=True)

    def filter_by_time(self, tasks: list[PetTask]) -> list[PetTask]:
        """Greedily select tasks in order until the remaining daily time budget is exhausted."""
        result = []
        remaining = self.available_minutes_per_day
        for task in tasks:
            if task.duration_minutes <= remaining:
                result.append(task)
                remaining -= task.duration_minutes
        return result


class DailyPlan:
    """Holds the final scheduled task list for one day and tracks cumulative duration."""

    def __init__(self, pets: list[Pet], date: str):
        """Initialize an empty plan for the given pets and ISO date string."""
        self.pets = pets
        self.date = date
        self.scheduled_tasks: list[PetTask] = []
        self.total_duration_minutes: int = 0

    def add_task(self, task: PetTask) -> None:
        """Append a task to the schedule and add its duration to the running total."""
        self.scheduled_tasks.append(task)
        self.total_duration_minutes += task.duration_minutes

    def display(self) -> str:
        """Format the full plan as a human-readable multi-line string with a totals footer."""
        pet_names = " & ".join(p.name for p in self.pets)
        lines = [f"Daily plan for {pet_names} — {self.date}"]
        for task in self.scheduled_tasks:
            lines.append(f"  • {task.get_summary()}")
        lines.append(f"Total: {self.total_duration_minutes} min")
        return "\n".join(lines)

    def get_summary(self) -> str:
        """Return a compact one-line overview of task count and total scheduled minutes."""
        return f"{len(self.scheduled_tasks)} tasks, {self.total_duration_minutes} min total"
