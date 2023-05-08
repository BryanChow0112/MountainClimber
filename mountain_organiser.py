from __future__ import annotations

from mountain import Mountain
from double_key_table import *
from infinite_hash_table import *
from algorithms.mergesort import mergesort
from algorithms.binary_search import binary_search

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountain_rank:list = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Finds the rank of the provided mountain given all mountains included so far. See below for an example.
        Raises KeyError if this mountain hasn't been added yet.

        should have complexity at most O(log(N)), where N is the total number of mountains
        included so far."""
        if mountain in self.mountain_rank:
            return binary_search(self.mountain_rank, mountain)
        else:
            raise KeyError("Mountain not in list")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds a list of mountains to the organiser
        if all the mountains you've seen are ranked by their length increasing. In cases where the length is the same,
        you should order them by name lexicographically increasing (you can assume this is unique)
        should have complexity at most O(Mlog(M)+N), where M is the length of the input list, and
        N is the total number of mountains included so far."""

        self.mountain_rank.extend(mountains)
        self.mountain_rank = mergesort(self.mountain_rank, key=lambda x: x.length)
