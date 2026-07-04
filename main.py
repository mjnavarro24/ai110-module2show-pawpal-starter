"""Demo script for the PawPal system.

Creates an owner with a couple of pets, gives those pets some tasks, then
prints today's schedule to the terminal.
"""

from datetime import date, time

from pawpal_system import (
    Owner,
    Pet,
    Priority,
    Scheduler,
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

    # Tasks are added out of chronological order on purpose, so the sorting
    # method has something to actually reorder.
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

    # An already-completed task, to show the completion filter at work.
    breakfast = Task(
        name="Breakfast",
        description="Morning meal for Whiskers.",
        priority=Priority.MEDIUM,
        duration_minutes=10,
        date=today,
        time=time(7, 0),
    )
    breakfast.mark_completed()
    whiskers.add_task(breakfast)

    return Owner(name="Alex", pets=[rex, whiskers])


def format_task(task: Task, pet_name: str) -> str:
    """One-line summary of a task for the terminal."""
    return (
        f"{task.time:%I:%M %p}  [{task.priority.name:<6}] "
        f"{task.name} ({pet_name}) — {task.duration_minutes} min"
    )


def print_todays_schedule(owner: Owner, scheduler: Scheduler) -> None:
    """Print today's tasks in time order using Scheduler.sort_by_time."""
    today = date.today()
    todays_tasks = scheduler.sort_by_time(owner.all_tasks(), on_day=today)

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
        print(format_task(task, task_to_pet.get(id(task), "?")))


def print_filtered_views(owner: Owner, scheduler: Scheduler) -> None:
    """Show Scheduler.filter_tasks by completion status and by pet name."""
    task_to_pet = {
        id(task): pet.name for pet in owner.pets for task in pet.tasks
    }

    def show(heading: str, tasks) -> None:
        print(f"\n{heading}")
        print("-" * 40)
        if not tasks:
            print("(none)")
            return
        for task in tasks:
            print(format_task(task, task_to_pet.get(id(task), "?")))

    show("Pending tasks", scheduler.filter_tasks(owner, completed=False))
    show("Completed tasks", scheduler.filter_tasks(owner, completed=True))
    show("Rex's tasks", scheduler.filter_tasks(owner, pet_name="Rex"))


def main() -> None:
    owner = build_owner()
    scheduler = Scheduler()
    print_todays_schedule(owner, scheduler)
    print_filtered_views(owner, scheduler)


if __name__ == "__main__":
    main()
