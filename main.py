from pawpal_system import Pet, PetTask, Scheduler

# --- Pet 1: Mochi ---
mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)
mochi.add_task(PetTask("Morning walk",  "walk",      30, "high"))
mochi.add_task(PetTask("Feeding",       "feed",      10, "high"))
mochi.add_task(PetTask("Grooming",      "grooming",  45, "low"))

# --- Pet 2: Luna ---
luna = Pet(name="Luna", species="cat", breed="Tabby", age=5)
luna.add_task(PetTask("Medication",  "medication",   5,  "high"))
luna.add_task(PetTask("Feeding",     "feed",         10, "medium"))
luna.add_task(PetTask("Playtime",    "enrichment",   20, "low"))

# --- One combined schedule for the owner (90 min budget) ---
scheduler = Scheduler(pets=[mochi, luna], available_minutes_per_day=90)
plan = scheduler.generate_plan()

# --- Print Today's Schedule ---
print("=" * 45)
print("           TODAY'S SCHEDULE")
print("=" * 45)
print()
print(plan.display())
print()
print(f"Summary: {plan.get_summary()}")
print("=" * 45)
