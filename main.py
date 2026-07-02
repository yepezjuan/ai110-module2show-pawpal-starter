from pawpal_system import Pet, PetTask, Scheduler

# --- Pet 1: Mochi (tasks added out of order: low before high) ---
mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)
mochi.add_task(PetTask("Grooming",      "grooming",  45, "low"))    # low, midday
mochi.add_task(PetTask("Morning walk",  "walk",      30, "high"))   # high, morning
mochi.add_task(PetTask("Feeding",       "feed",      10, "high"))   # high, morning

# --- Pet 2: Luna (tasks added out of order: evening before morning) ---
luna = Pet(name="Luna", species="cat", breed="Tabby", age=5)
luna.add_task(PetTask("Playtime",    "enrichment",  20, "low"))    # low, evening
luna.add_task(PetTask("Feeding",     "feed",        10, "medium")) # medium, morning
luna.add_task(PetTask("Medication",  "medication",   5, "high"))   # high, morning

# Mark one task complete to demonstrate status filtering
mochi.tasks[0].mark_complete()   # Grooming is done

# --- Build scheduler ---
scheduler = Scheduler(pets=[mochi, luna], available_minutes_per_day=90)
all_tasks = [t for pet in [mochi, luna] for t in pet.get_tasks()]

print("=" * 45)
print("  FILTER: Mochi's tasks only")
print("=" * 45)
mochi_tasks = scheduler.filter_by_pet(all_tasks, "Mochi")
for t in mochi_tasks:
    print(f"  {t.get_summary()}")

print()
print("=" * 45)
print("  FILTER: incomplete tasks only")
print("=" * 45)
incomplete = scheduler.filter_by_status(all_tasks, completed=False)
for t in incomplete:
    print(f"  {t.get_summary()}")

print()
print("=" * 45)
print("  FILTER: completed tasks only")
print("=" * 45)
done = scheduler.filter_by_status(all_tasks, completed=True)
for t in done:
    print(f"  {t.get_summary()}")

print()
print("=" * 45)
print("  SORTED: all tasks by slot + priority")
print("=" * 45)
sorted_tasks = scheduler.sort_by_time_and_priority(all_tasks)
for t in sorted_tasks:
    print(f"  {t.get_summary()}")

print()
print("=" * 45)
print("       TODAY'S SCHEDULE")
print("=" * 45)
plan = scheduler.generate_plan()
print(plan.display())
print()
print(f"Summary: {plan.get_summary()}")
print("=" * 45)
