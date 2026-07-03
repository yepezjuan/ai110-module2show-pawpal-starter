import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, PetTask, Scheduler


def test_mark_complete_changes_status():
    task = PetTask(title="Morning walk", task_type="walk", duration_minutes=30, priority="high")
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=3)
    assert len(pet.tasks) == 0
    task = PetTask(title="Feed breakfast", task_type="feed", duration_minutes=10, priority="medium")
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sort_by_time_and_priority_orders_correctly():
    scheduler = Scheduler(pets=[], available_minutes_per_day=999)

    task_evening = PetTask(title="Evening enrichment", task_type="enrichment", duration_minutes=20, priority="low", time_slot="evening")
    task_morning_low = PetTask(title="Morning feed", task_type="feed", duration_minutes=10, priority="low", time_slot="morning")
    task_morning_high_med = PetTask(title="Morning medication", task_type="medication", duration_minutes=5, priority="high", time_slot="morning")

    result = scheduler.sort_by_time_and_priority([task_evening, task_morning_low, task_morning_high_med])

    assert result[0] is task_morning_high_med  # morning + high priority + medication type
    assert result[1] is task_morning_low        # morning + low priority + feed type
    assert result[2] is task_evening            # evening slot comes last


def test_recurring_task_reappears_after_reset():
    pet = Pet(name="Luna", species="cat", breed="Siamese", age=2)
    task = PetTask(title="Daily medication", task_type="medication", duration_minutes=5, priority="high")
    pet.add_task(task)
    scheduler = Scheduler(pets=[pet], available_minutes_per_day=60)

    task.mark_complete()
    assert task.is_complete is True

    pet.reset_recurring_tasks()
    assert task.is_complete is False

    plan = scheduler.generate_plan()
    assert task in plan.scheduled_tasks


def test_non_recurring_task_stays_complete_after_reset():
    pet = Pet(name="Rex", species="dog", breed="Poodle", age=5)
    task = PetTask(title="One-time grooming", task_type="grooming", duration_minutes=30, priority="medium", recurring=False)
    pet.add_task(task)
    scheduler = Scheduler(pets=[pet], available_minutes_per_day=60)

    task.mark_complete()
    pet.reset_recurring_tasks()

    assert task.is_complete is True
    plan = scheduler.generate_plan()
    assert task not in plan.scheduled_tasks


def test_slot_overflow_is_flagged_as_conflict():
    pet = Pet(name="Max", species="dog", breed="Beagle", age=4)
    task_big = PetTask(title="Long walk", task_type="walk", duration_minutes=170, priority="medium", time_slot="morning")
    task_extra = PetTask(title="Extra feed", task_type="feed", duration_minutes=20, priority="low", time_slot="morning")
    pet.add_task(task_big)
    pet.add_task(task_extra)

    scheduler = Scheduler(pets=[pet], available_minutes_per_day=500)
    plan = scheduler.generate_plan()

    assert task_big in plan.scheduled_tasks
    assert task_extra in [t for t, _ in plan.conflicts]
    assert "morning slot full (180 min max)" in [r for _, r in plan.conflicts]


def test_daily_budget_overflow_is_flagged_as_conflict():
    pet = Pet(name="Bella", species="dog", breed="Husky", age=2)
    task = PetTask(title="All-day adventure", task_type="walk", duration_minutes=90, priority="high", time_slot="anytime")
    pet.add_task(task)

    scheduler = Scheduler(pets=[pet], available_minutes_per_day=60)
    plan = scheduler.generate_plan()

    assert task not in plan.scheduled_tasks
    assert task in [t for t, _ in plan.conflicts]
    assert "exceeds daily time budget" in [r for _, r in plan.conflicts]
