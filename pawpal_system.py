"""PawPal system core implementation.

Generated from diagrams/uml_draft.mmd, then fleshed out with core logic.
"""

from dataclasses import dataclass, field
from datetime import date, time, datetime, timedelta
from enum import IntEnum
from typing import List


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

        total_minutes = sum(task.duration_minutes for task in scheduled)
        explanation = (
            f"Scheduled {len(scheduled)} task(s) for {owner.name}, "
            f"totaling {total_minutes} minutes, ordered by priority then time."
        )

        plan = Plan(tasks=scheduled, explanation=explanation)
        owner.schedule = plan
        return plan
