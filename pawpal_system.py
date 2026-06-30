from dataclasses import dataclass, field


@dataclass
class PetTask:
    title: str
    task_type: str          # "walk", "feed", "medication", "grooming", "enrichment", "other"
    duration_minutes: int
    priority: str           # "low", "medium", "high"

    def get_summary(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[PetTask] = field(default_factory=list)

    def add_task(self, task: PetTask) -> None:
        pass

    def remove_task(self, task: PetTask) -> None:
        pass

    def get_tasks(self) -> list[PetTask]:
        pass


PRIORITY_ORDER = {"low": 0, "medium": 1, "high": 2}


class Scheduler:
    def __init__(self, pet: Pet, available_minutes_per_day: int):
        self.pet = pet
        self.available_minutes_per_day = available_minutes_per_day

    def generate_plan(self) -> "DailyPlan":
        pass

    def sort_by_priority(self, tasks: list[PetTask]) -> list[PetTask]:
        pass

    def filter_by_time(self, tasks: list[PetTask]) -> list[PetTask]:
        pass


class DailyPlan:
    def __init__(self, pet: Pet, date: str):
        self.pet = pet
        self.date = date
        self.scheduled_tasks: list[PetTask] = []
        self.total_duration_minutes: int = 0

    def add_task(self, task: PetTask) -> None:
        pass

    def display(self) -> str:
        pass

    def get_summary(self) -> str:
        pass
