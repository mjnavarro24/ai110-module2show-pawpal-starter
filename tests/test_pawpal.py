"""Simple tests for the PawPal system."""

from datetime import date, time

from pawpal_system import Owner, Pet, Priority, Recurrence, Scheduler, Task


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


def test_identical_start_times_conflict():
    """Two tasks starting at the exact same time are flagged as a conflict."""
    walk = make_task("Walk", start=time(9, 0), duration_minutes=30)
    feed = make_task("Feed", start=time(9, 0), duration_minutes=30)

    assert Scheduler().find_conflicts([walk, feed]) == [(walk, feed)]


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


def test_break_early_exit_still_catches_later_overlap():
    """A non-overlapping middle task must not hide a later true overlap.

    find_conflicts breaks its inner scan once a later task starts at/after the
    current one ends. A long task must still be compared against a task that
    starts after a shorter, non-overlapping one earlier in the sorted order.
    """
    long = make_task("Long", start=time(9, 0), duration_minutes=120)   # 9:00-11:00
    gap = make_task("Gap", start=time(11, 0), duration_minutes=15)     # 11:00-11:15, no overlap
    late = make_task("Late", start=time(10, 30), duration_minutes=30)  # 10:30-11:00, overlaps long

    conflicts = Scheduler().find_conflicts([long, gap, late])

    # Only long/late overlap; gap butts up against long but does not conflict.
    assert conflicts == [(long, late)]


def test_sort_by_time_orders_todays_tasks():
    """sort_by_time returns the day's tasks in time-of-day order."""
    late = make_task("Late", start=time(17, 0))
    early = make_task("Early", start=time(6, 0))
    noon = make_task("Noon", start=time(12, 0))

    ordered = Scheduler().sort_by_time([late, early, noon], on_day=date(2026, 7, 1))

    assert ordered == [early, noon, late]


def test_sort_by_time_excludes_other_days():
    """Only tasks scheduled for on_day are included."""
    today_task = make_task("Today", start=time(9, 0))
    other_day = Task(
        name="Other",
        description="",
        priority=Priority.MEDIUM,
        duration_minutes=30,
        date=date(2026, 7, 2),
        time=time(8, 0),
    )

    ordered = Scheduler().sort_by_time([today_task, other_day], on_day=date(2026, 7, 1))

    assert ordered == [today_task]


def test_filter_tasks_by_completion_status():
    """filter_tasks keeps only tasks matching the completed flag."""
    pet = Pet(name="Rex", age=3)
    done = make_task("Done")
    done.mark_completed()
    todo = make_task("Todo")
    pet.add_task(done)
    pet.add_task(todo)
    owner = Owner(name="Sam", pets=[pet])

    assert owner.filter_tasks(completed=True) == [done]
    assert owner.filter_tasks(completed=False) == [todo]


def test_filter_tasks_by_pet_name():
    """filter_tasks keeps only tasks belonging to the named pet."""
    rex = Pet(name="Rex", age=3)
    rex_task = make_task("Walk Rex")
    rex.add_task(rex_task)
    milo = Pet(name="Milo", age=2)
    milo.add_task(make_task("Walk Milo"))
    owner = Owner(name="Sam", pets=[rex, milo])

    assert owner.filter_tasks(pet_name="Rex") == [rex_task]


def test_filter_tasks_with_no_filters_returns_all():
    """Passing no filters returns every task across all pets."""
    pet = Pet(name="Rex", age=3)
    pet.add_task(make_task("A"))
    pet.add_task(make_task("B"))
    owner = Owner(name="Sam", pets=[pet])

    assert len(owner.filter_tasks()) == 2


def test_complete_task_one_off_spawns_nothing():
    """Completing a non-recurring task creates no new task."""
    pet = Pet(name="Rex", age=3)
    task = make_task("Walk")
    pet.add_task(task)

    result = pet.complete_task(task)

    assert result is None
    assert task.is_completed
    assert len(pet.tasks) == 1


def test_complete_daily_task_spawns_next_day():
    """Completing a daily task adds a pending copy one day later."""
    pet = Pet(name="Rex", age=3)
    task = make_task("Feed", start=time(8, 0))
    task.recurrence = Recurrence.DAILY
    pet.add_task(task)

    upcoming = pet.complete_task(task)

    assert upcoming is not None
    assert upcoming.date == date(2026, 7, 2)
    assert upcoming.time == time(8, 0)
    assert upcoming.recurrence == Recurrence.DAILY
    assert not upcoming.is_completed
    assert pet.tasks == [task, upcoming]


def test_complete_weekly_task_spawns_next_week():
    """Completing a weekly task adds a pending copy seven days later."""
    pet = Pet(name="Rex", age=3)
    task = make_task("Grooming", start=time(10, 0))
    task.recurrence = Recurrence.WEEKLY
    pet.add_task(task)

    upcoming = pet.complete_task(task)

    assert upcoming.date == date(2026, 7, 8)


def test_complete_task_is_idempotent():
    """Completing an already-done task does not spawn a duplicate."""
    pet = Pet(name="Rex", age=3)
    task = make_task("Feed")
    task.recurrence = Recurrence.DAILY
    pet.add_task(task)

    pet.complete_task(task)
    second = pet.complete_task(task)

    assert second is None
    assert len(pet.tasks) == 2  # original + one spawned copy, no more


def test_generate_schedule_carries_conflicts():
    """The generated Plan surfaces conflicts and notes them in the explanation."""
    pet = Pet(name="Rex", age=3)
    pet.add_task(make_task("Walk", start=time(9, 0), duration_minutes=30))
    pet.add_task(make_task("Feed", start=time(9, 15), duration_minutes=30))
    owner = Owner(name="Sam", pets=[pet])

    plan = Scheduler().generate_schedule(owner)

    assert len(plan.conflicts) == 1
    assert "conflict" in plan.explanation.lower()


def test_all_tasks_spans_multiple_pets():
    """all_tasks aggregates tasks across every pet the owner has."""
    rex = Pet(name="Rex", age=3)
    rex.add_task(make_task("Walk Rex"))
    milo = Pet(name="Milo", age=2)
    milo.add_task(make_task("Walk Milo"))
    milo.add_task(make_task("Feed Milo"))
    owner = Owner(name="Sam", pets=[rex, milo])

    assert len(owner.all_tasks()) == 3


def test_pending_tasks_spans_multiple_pets():
    """pending_tasks excludes completed tasks across all pets."""
    rex = Pet(name="Rex", age=3)
    rex_done = make_task("Walk Rex")
    rex.add_task(rex_done)
    milo = Pet(name="Milo", age=2)
    milo_task = make_task("Walk Milo")
    milo.add_task(milo_task)
    owner = Owner(name="Sam", pets=[rex, milo])

    rex.complete_task(rex_done)

    assert owner.pending_tasks() == [milo_task]


def test_find_conflicts_across_pets():
    """A conflict is detected between two different pets' overlapping tasks."""
    rex = Pet(name="Rex", age=3)
    rex_vet = make_task("Vet visit", start=time(15, 0), duration_minutes=60)
    rex.add_task(rex_vet)
    milo = Pet(name="Milo", age=2)
    milo_feed = make_task("Feed Milo", start=time(15, 30), duration_minutes=15)
    milo.add_task(milo_feed)
    owner = Owner(name="Sam", pets=[rex, milo])

    conflicts = Scheduler().find_conflicts(owner.all_tasks())

    assert conflicts == [(rex_vet, milo_feed)]


def test_generate_schedule_orders_across_pets_by_priority():
    """generate_schedule orders tasks from different pets by priority, then time."""
    rex = Pet(name="Rex", age=3)
    rex_low = make_task("Low Rex", start=time(8, 0))
    rex_low.priority = Priority.LOW
    rex.add_task(rex_low)
    milo = Pet(name="Milo", age=2)
    milo_high = make_task("High Milo", start=time(17, 0))
    milo_high.priority = Priority.HIGH
    milo.add_task(milo_high)
    owner = Owner(name="Sam", pets=[rex, milo])

    plan = Scheduler().generate_schedule(owner)

    # Higher priority wins even though its time is later in the day.
    assert [task.name for task in plan.tasks] == ["High Milo", "Low Rex"]
