from datetime import date, time

import streamlit as st

from pawpal_system import Priority, Recurrence, Task, Pet, Plan, Owner, Scheduler

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

# --- Owner setup (runs once) ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)

st.session_state.owner.name = owner_name  # keep in sync with the input

# --- Add a pet ---
st.markdown("### Pets")
pcol1, pcol2 = st.columns(2)
with pcol1:
    new_pet_name = st.text_input("New pet name", value="")
with pcol2:
    new_pet_age = st.number_input("Age", min_value=0, max_value=40, value=0)

if st.button("Add pet"):
    name = new_pet_name.strip()
    existing = [pet.name for pet in st.session_state.owner.pets]
    if not name:
        st.warning("Give the pet a name first.")
    elif name in existing:
        st.warning(f"You already have a pet named '{name}'.")
    else:
        st.session_state.owner.pets.append(Pet(name=name, age=int(new_pet_age)))
        st.success(f"Added {name}.")
        st.rerun()

if st.session_state.owner.pets:
    st.caption(
        "Your pets: "
        + ", ".join(f"{pet.name} ({pet.age})" for pet in st.session_state.owner.pets)
    )
else:
    st.info("Add a pet to get started.")

PRIORITY_MAP = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
RECURRENCE_MAP = {
    "none": Recurrence.NONE,
    "daily": Recurrence.DAILY,
    "weekly": Recurrence.WEEKLY,
}

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

pets = st.session_state.owner.pets
if not pets:
    st.info("Add a pet above before creating tasks.")
else:
    selected_pet_name = st.selectbox("Add task for pet", [pet.name for pet in pets])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["none", "daily", "weekly"])

    if st.button("Add task"):
        pet = next(pet for pet in pets if pet.name == selected_pet_name)
        # Give each task a distinct time (in add order) so same-priority tasks stay ordered.
        new_task = Task(
            name=task_title,
            description="",
            priority=PRIORITY_MAP[priority],
            duration_minutes=int(duration),
            date=date.today(),
            time=time(hour=min(8 + len(pet.tasks), 23)),
            recurrence=RECURRENCE_MAP[frequency],
        )
        pet.add_task(new_task)

# Map each task back to the pet it belongs to, for a "Pet" column in tables.
pet_of = {
    id(task): pet.name
    for pet in st.session_state.owner.pets
    for task in pet.tasks
}

all_tasks = st.session_state.owner.all_tasks()
if all_tasks:
    st.write("Current tasks:")

    fcol1, fcol2 = st.columns(2)
    with fcol1:
        status_filter = st.selectbox(
            "Filter by status", ["All", "Pending", "Completed"]
        )
    with fcol2:
        pet_names = [pet.name for pet in st.session_state.owner.pets]
        pet_filter = st.selectbox("Filter by pet", ["All"] + pet_names)

    completed = {"All": None, "Pending": False, "Completed": True}[status_filter]
    selected_pet = None if pet_filter == "All" else pet_filter

    filtered_tasks = st.session_state.owner.filter_tasks(
        completed=completed, pet_name=selected_pet
    )

    if filtered_tasks:
        st.table(
            [
                {
                    "Pet": pet_of.get(id(task), "?"),
                    "Task": task.name,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority.name,
                    "Frequency": task.recurrence.value,
                    "Status": task.status,
                }
                for task in filtered_tasks
            ]
        )
    else:
        st.info("No tasks match the selected filters.")

    # Mark-complete control: pick a pending task and complete it. Recurring
    # tasks spawn their next occurrence via Pet.complete_task.
    pending = [
        (pet, task)
        for pet in st.session_state.owner.pets
        for task in pet.tasks
        if not task.is_completed
    ]
    if pending:
        st.markdown("#### Mark a task complete")
        choice = st.selectbox(
            "Pending task",
            options=range(len(pending)),
            format_func=lambda i: f"{pending[i][1].name} ({pending[i][0].name})",
        )
        if st.button("Mark complete"):
            pet, task = pending[choice]
            spawned = pet.complete_task(task)
            if spawned:
                st.success(
                    f"Completed '{task.name}'. Next {task.recurrence.value} "
                    f"occurrence scheduled for {spawned.date}."
                )
            else:
                st.success(f"Completed '{task.name}'.")
            st.rerun()

    # Remove-task control: pick any task and delete it from its pet.
    removable = [
        (pet, task)
        for pet in st.session_state.owner.pets
        for task in pet.tasks
    ]
    if removable:
        st.markdown("#### Remove a task")
        rm_choice = st.selectbox(
            "Task to remove",
            options=range(len(removable)),
            format_func=lambda i: f"{removable[i][1].name} ({removable[i][0].name})",
            key="remove_select",
        )
        if st.button("Remove task"):
            pet, task = removable[rm_choice]
            pet.remove_task(task)
            st.success(f"Removed '{task.name}'.")
            st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Today's Timeline")
st.caption("All of today's tasks ordered by time of day.")

todays_tasks = Scheduler().sort_by_time(
    st.session_state.owner.all_tasks(), on_day=date.today()
)
if todays_tasks:
    st.table(
        [
            {
                "Time": task.time.strftime("%H:%M"),
                "Pet": pet_of.get(id(task), "?"),
                "Task": task.name,
                "Priority": task.priority.name,
                "Duration (min)": task.duration_minutes,
                "Status": task.status,
            }
            for task in todays_tasks
        ]
    )
else:
    st.info("No tasks scheduled for today.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan = scheduler.generate_schedule(st.session_state.owner)

    if plan.tasks:
        st.success(plan.explanation)
        st.table(
            [
                {
                    "Time": task.time.strftime("%H:%M"),
                    "Pet": pet_of.get(id(task), "?"),
                    "Task": task.name,
                    "Priority": task.priority.name,
                    "Duration (min)": task.duration_minutes,
                }
                for task in plan.tasks
            ]
        )

        if plan.conflicts:
            st.warning(f"⚠️ {len(plan.conflicts)} time conflict(s) detected:")
            st.table(
                [
                    {
                        "Task A": f"{a.name} ({pet_of.get(id(a), '?')})",
                        "A time": f"{a.time.strftime('%H:%M')}–{a.ends_at.strftime('%H:%M')}",
                        "Task B": f"{b.name} ({pet_of.get(id(b), '?')})",
                        "B time": f"{b.time.strftime('%H:%M')}–{b.ends_at.strftime('%H:%M')}",
                    }
                    for a, b in plan.conflicts
                ]
            )
    else:
        st.info("No pending tasks to schedule. Add a task above first.")
