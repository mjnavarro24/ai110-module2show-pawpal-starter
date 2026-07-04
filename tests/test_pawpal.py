"""Simple tests for the PawPal system."""

from datetime import date, time

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def make_task(name="Walk", start=time(9, 0), duration_minutes=30):
    return Task(
        name=name,
        description="",
        priority=Priority.MEDIUM,
        duration_minutes=duration_minutes,
        date=date(2026, 7, 1),
        time=start,
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


def test_overlapping_tasks_are_flagged():
    """Two tasks sharing time are reported as one conflict pair."""
    walk = make_task("Walk", start=time(9, 0), duration_minutes=30)
    feed = make_task("Feed", start=time(9, 15), duration_minutes=30)

    conflicts = Scheduler().find_conflicts([walk, feed])

    assert conflicts == [(walk, feed)]


def test_back_to_back_tasks_do_not_conflict():
    """One task ending exactly when the next starts is not a conflict."""
    walk = make_task("Walk", start=time(9, 0), duration_minutes=30)
    feed = make_task("Feed", start=time(9, 30), duration_minutes=30)

    assert Scheduler().find_conflicts([walk, feed]) == []


def test_zero_duration_task_never_conflicts():
    """A zero-length task shares no interval with anything."""
    walk = make_task("Walk", start=time(9, 0), duration_minutes=30)
    note = make_task("Note", start=time(9, 15), duration_minutes=0)

    assert Scheduler().find_conflicts([walk, note]) == []


def test_three_way_pileup_reports_each_pair():
    """Three mutually overlapping tasks yield all three pairs."""
    a = make_task("A", start=time(9, 0), duration_minutes=60)
    b = make_task("B", start=time(9, 15), duration_minutes=60)
    c = make_task("C", start=time(9, 30), duration_minutes=60)

    conflicts = Scheduler().find_conflicts([a, b, c])

    # Reported in sorted-by-start order; Task isn't hashable, so compare as a list.
    assert conflicts == [(a, b), (a, c), (b, c)]


def test_generate_schedule_carries_conflicts():
    """The generated Plan surfaces conflicts and notes them in the explanation."""
    pet = Pet(name="Rex", age=3)
    pet.add_task(make_task("Walk", start=time(9, 0), duration_minutes=30))
    pet.add_task(make_task("Feed", start=time(9, 15), duration_minutes=30))
    owner = Owner(name="Sam", pets=[pet])

    plan = Scheduler().generate_schedule(owner)

    assert len(plan.conflicts) == 1
    assert "conflict" in plan.explanation.lower()
