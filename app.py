import streamlit as st
from pawpal_system import PetTask, Pet, Scheduler, DailyPlan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="Mixed")
age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_type = st.selectbox("Type", ["walk", "feed", "medication", "grooming", "enrichment", "other"])
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task = PetTask(
        title=task_title,
        task_type=task_type,
        duration_minutes=int(duration),
        priority=priority,
    )
    st.session_state.tasks.append(task)

if st.session_state.tasks:
    st.write("Current tasks (sorted by slot → priority):")
    preview_scheduler = Scheduler(pets=[], available_minutes_per_day=9999)
    sorted_preview = preview_scheduler.sort_by_time_and_priority(st.session_state.tasks)
    for t in sorted_preview:
        st.write(f"- {t.get_summary()}")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=120)

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        pet = Pet(name=pet_name, species=species, breed=breed, age=int(age))
        for task in st.session_state.tasks:
            pet.add_task(task)
        scheduler = Scheduler(pets=[pet], available_minutes_per_day=int(available_minutes))
        plan = scheduler.generate_plan()
        st.session_state.plan = plan

if "plan" in st.session_state and st.session_state.plan:
    plan = st.session_state.plan

    # Summary metrics row
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Scheduled tasks", len(plan.scheduled_tasks))
    col_b.metric("Total time (min)", plan.total_duration_minutes)
    col_c.metric("Conflicts", len(plan.conflicts))

    # Scheduled tasks grouped by time slot
    if plan.scheduled_tasks:
        st.markdown("#### Scheduled tasks")
        current_slot = None
        for task in plan.scheduled_tasks:
            if task.time_slot != current_slot:
                current_slot = task.time_slot
                st.markdown(f"**{current_slot.upper()}**")
            st.write(f"  • {task.get_summary()}")
    else:
        st.info("No tasks fit within your available time.")

    # Conflict warnings — one st.warning per skipped task
    if plan.conflicts:
        st.markdown("#### Not scheduled")
        for task, reason in plan.conflicts:
            st.warning(f"**{task.title}** ({task.pet_name}) — {reason}")
