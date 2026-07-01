"""Simple tests for the PawPal system."""

from datetime import date, time

from pawpal_system import Pet, Priority, Task


def make_task(name="Walk"):
    return Task(
        name=name,
        description="",
        priority=Priority.MEDIUM,
        duration_minutes=30,
        date=date(2026, 7, 1),
        time=time(9, 0),
    )


def test_mark_complete_changes_status():
    """Task Completion: mark_completed() flips the task's status."""
    task = make_task()
    assert task.status == "pending"

    task.mark_completed()

    assert task.status == "completed"
    assert task.is_completed


def test_add_task_increases_pet_task_count():
    """Task Addition: adding a task raises the pet's task count."""
    pet = Pet(name="Rex", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(make_task())

    assert len(pet.tasks) == 1
