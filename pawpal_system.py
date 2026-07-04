"""PawPal system core implementation.

Generated from diagrams/uml_draft.mmd, then fleshed out with core logic.
"""

from dataclasses import dataclass, field
from datetime import date, time, datetime, timedelta
from enum import IntEnum
from typing import List, Tuple


class Priority(IntEnum):
    """Task importance. Higher value = more urgent, so it sorts first."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


# class Weekday(IntEnum):
#     """Matches datetime.weekday(): Monday is 0, Sunday is 6."""

#     MONDAY = 0
#     TUESDAY = 1
#     WEDNESDAY = 2
#     THURSDAY = 3
#     FRIDAY = 4
#     SATURDAY = 5
#     SUNDAY = 6


# @dataclass(frozen=True)
# class TimeWindow:
#     """A recurring weekly span the owner is free, e.g. 'every Monday 6–9pm'."""

#     day: Weekday
#     start: time
#     end: time

#     def fits(self, moment: datetime, duration_minutes: int) -> bool:
#         """True if a task starting at `moment` for `duration_minutes` sits inside this window."""
#         if moment.weekday() != self.day:
#             return False
#         end_moment = (moment + timedelta(minutes=duration_minutes)).time()
#         return self.start <= moment.time() and end_moment <= self.end


# # When the owner is available, as a set of recurring weekly windows.
# Availability = List[TimeWindow]


@dataclass
class Task:
    name: str
    description: str
    priority: Priority
    duration_minutes: int
    date: date
    time: time
    status: str = "pending"  # e.g., "pending", "completed"

    @property
    def scheduled_for(self) -> datetime:
        # Combined date + time, convenient for sorting/comparison.
        return datetime.combine(self.date, self.time)
    
    @property
    def ends_at(self) -> datetime:
        # When this task finishes.
        return self.scheduled_for + timedelta(minutes=self.duration_minutes)

    def overlaps(self, other: "Task") -> bool:
        # True if this task's time interval intersects another's.
        # Half-open intervals: back-to-back tasks (one ends exactly when
        # the next starts) do NOT count as a conflict. A zero-duration task
        # is an empty interval, so it never overlaps anything.
        if self.duration_minutes == 0 or other.duration_minutes == 0:
            return False
        return self.scheduled_for < other.ends_at and other.scheduled_for < self.ends_at

    @property
    def is_completed(self) -> bool:
        # True if this task's status is 'completed'.
        return self.status == "completed"

    def mark_completed(self) -> None:
        # Set this task's status to 'completed'.
        self.status = "completed"

    def mark_pending(self) -> None:
        # Set this task's status back to 'pending'.

        self.status = "pending"


@dataclass
class Pet:
    name: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        # Add a task to this pet, ignoring duplicates.

        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
         # Remove a task from this pet if it is present.
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Plan:
    tasks: List[Task] = field(default_factory=list)
    explanation: str = ""
    # Pairs of tasks whose scheduled times overlap.
    conflicts: List[Tuple[Task, Task]] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    # availability: Availability
    pets: List[Pet] = field(default_factory=list)
    schedule: Plan = field(default_factory=Plan)

    def all_tasks(self) -> List[Task]:
        # Every task across all of this owner's pets.
        return [task for pet in self.pets for task in pet.tasks]

    # Every not-yet-completed task across all of this owner's pets.
    def pending_tasks(self) -> List[Task]:
        return [task for task in self.all_tasks() if not task.is_completed]


@dataclass
class Scheduler:
    def find_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """Return every pair of tasks whose scheduled times overlap.

        Sorts by start time, then compares each task only against those it
        could still overlap — once a later task starts at/after this one
        ends, nothing further can overlap it either, so we stop scanning.
        """
        ordered = sorted(tasks, key=lambda t: t.scheduled_for)
        conflicts: List[Tuple[Task, Task]] = []

        for i, task in enumerate(ordered):
            for later in ordered[i + 1:]:
                if later.scheduled_for >= task.ends_at:
                    break
                if task.overlaps(later):
                    conflicts.append((task, later))

        return conflicts

    def sort_by_time(self, tasks: List[Task], on_day: date = None) -> List[Task]:
        """Return a day's tasks ordered by their time-of-day attribute.

        Only tasks scheduled for `on_day` (defaults to today) are included,
        so ordering by the time-of-day attribute alone gives a correct
        chronological order.
        """
        if on_day is None:
            on_day = date.today()
        days_tasks = [task for task in tasks if task.date == on_day]
        return sorted(days_tasks, key=lambda task: task.time)

    def filter_tasks(
        self, owner: Owner, completed: bool = None, pet_name: str = None
    ) -> List[Task]:
        """Return the owner's tasks filtered by completion status and/or pet name.

        Both filters are optional. Passing neither returns every task; passing
        both keeps only tasks matching both conditions.
        """
        tasks = []
        for pet in owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.is_completed != completed:
                    continue
                tasks.append(task)
        return tasks

    def generate_schedule(self, owner: Owner) -> Plan:
        """Build a Plan from the owner's pending tasks.

        Tasks are ordered by priority (highest first), then by the time they
        are scheduled for. The resulting Plan is stored on the owner and
        returned so the two stay in sync.
        """
        scheduled = sorted(
            owner.pending_tasks(),
            key=lambda task: (-int(task.priority), task.scheduled_for),
        )

        conflicts = self.find_conflicts(scheduled)

        total_minutes = sum(task.duration_minutes for task in scheduled)
        explanation = (
            f"Scheduled {len(scheduled)} task(s) for {owner.name}, "
            f"totaling {total_minutes} minutes, ordered by priority then time."
        )
        if conflicts:
            explanation += f" ⚠️ {len(conflicts)} time conflict(s) detected."

        plan = Plan(tasks=scheduled, explanation=explanation, conflicts=conflicts)
        owner.schedule = plan
        return plan
