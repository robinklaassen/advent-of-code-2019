from enum import Enum, auto
from typing import Optional

from dataclasses import dataclass


class State(Enum):
    UNKNOWN = -1
    EMPTY = 0
    WALL = 1
    TARGET = 2
    OXYGENATED = 3
    

@dataclass(frozen=True)  # immutable, therefore hashable
class Node:
    """A node on the grid."""
    x: int
    y: int
    state: State
    value: Optional[int]
