from __future__ import annotations

from mountain import Mountain
from algorithms.mergesort import mergesort
from algorithms.binary_search import binary_search


class MountainOrganiser:

    def __init__(self) -> None:
        """
        Initialise the MountainOrganiser.

        Complexity
        - Worst case: O(1), initialisation operation is a constant time operation.
        - Best case: O(1), same as worst case

        """
        self.mountain_rank: list = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        Finds the rank of the provided mountain given all mountains included so far.
        Raises KeyError if this mountain hasn't been added yet.

        Complexity
        - Worst case: O(log (N)), where N is the total number of mountains included so far 
          (time complexity of binary search)
        - Best case: O(1), when the mountain is the first item in the sorted list.

        """
        if mountain in self.mountain_rank:  # check if mountain is in list
            return binary_search(self.mountain_rank, mountain)  # use binary search to find its index
        else:
            raise KeyError("Mountain not in list")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds a list of mountains to the organiser.

        Complexity
        - Worst case: O(M log(M) + N), where M is the length of the input list and N is the total number of mountains
          included so far. (when the input list is in reverse order)
        - Best case: O(M log(M) + N), same as worst case (when the input list is sorted)

        """

        self.mountain_rank.extend(mountains)
        # Sort the mountain_rank list using mergesort, with the length of the mountain as key
        self.mountain_rank = mergesort(self.mountain_rank, key=lambda x: x.length)
