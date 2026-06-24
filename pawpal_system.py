"""PawPal system skeleton.

Generated from diagrams/uml_draft.mmd. Method bodies are stubs to be filled in.
"""

from dataclasses import dataclass, field
from datetime import date, time
from typing import List


# Placeholder types referenced in the UML. Replace with real implementations
# (e.g. an Enum for Priority, an int of minutes for Duration) as the design firms up.
Availability = str
Priority = str


@dataclass
class Pet:
    name: str
    age: int


@dataclass
class Task:
    name: str
    priority: Priority
    duration_minutes: int
    date: date
    time: time


@dataclass
class Plan:
    tasks: List[Task] = field(default_factory=list)
    explanation: str = ""


@dataclass
class ToDoList:
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError

    def edit_task(self, task: Task) -> None:
        raise NotImplementedError

    def generate_schedule(self) -> Plan:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    availability: Availability
    pets: List[Pet] = field(default_factory=list)
    todo_list: ToDoList = field(default_factory=ToDoList)

    def edit_availability(self, availability: Availability) -> None:
        raise NotImplementedError
