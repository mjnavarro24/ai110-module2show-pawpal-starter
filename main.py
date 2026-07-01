"""Demo script for the PawPal system.

Creates an owner with a couple of pets, gives those pets some tasks, then
prints today's schedule to the terminal.
"""

from datetime import date, time

from pawpal_system import (
    Owner,
    Pet,
    Priority,
    Task,
)


def build_owner() -> Owner:
    """Assemble an owner, their pets, and a handful of tasks for today."""
    today = date.today()

    # The owner is free all day today, whatever weekday that happens to be.
    # availability = [
    #     TimeWindow(
    #         day=Weekday(today.weekday()),
    #         start=time(0, 0),
    #         end=time(23, 59),
    #     )
    # ]

    rex = Pet(name="Rex", age=4)
    whiskers = Pet(name="Whiskers", age=2)

    rex.add_task(
        Task(
            name="Morning walk",
            description="Walk Rex around the block.",
            priority=Priority.HIGH,
            duration_minutes=30,
            date=today,
            time=time(8, 0),
        )
    )
    rex.add_task(
        Task(
            name="Vet appointment",
            description="Annual checkup for Rex.",
            priority=Priority.MEDIUM,
            duration_minutes=60,
            date=today,
            time=time(15, 0),
        )
    )
    whiskers.add_task(
        Task(
            name="Feed Whiskers",
            description="Evening meal for Whiskers.",
            priority=Priority.HIGH,
            duration_minutes=10,
            date=today,
            time=time(18, 30),
        )
    )

    return Owner(name="Alex", pets=[rex, whiskers])


def print_todays_schedule(owner: Owner) -> None:
    """Print every task scheduled for today, earliest first."""
    today = date.today()
    todays_tasks = sorted(
        (task for task in owner.all_tasks() if task.date == today),
        key=lambda task: task.time,
    )

    print("Today's Schedule")
    print("=" * 40)
    print(f"{owner.name} — {today:%A, %B %d, %Y}\n")

    if not todays_tasks:
        print("Nothing scheduled for today.")
        return

    # Map each task back to the pet it belongs to for a friendlier printout.
    task_to_pet = {
        id(task): pet.name for pet in owner.pets for task in pet.tasks
    }

    for task in todays_tasks:
        pet_name = task_to_pet.get(id(task), "?")
        print(
            f"{task.time:%I:%M %p}  [{task.priority.name:<6}] "
            f"{task.name} ({pet_name}) — {task.duration_minutes} min"
        )


def main() -> None:
    owner = build_owner()
    print_todays_schedule(owner)


if __name__ == "__main__":
    main()
