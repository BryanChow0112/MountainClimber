from mountain import Mountain
from double_key_table import DoubleKeyTable
from algorithms.mergesort import mergesort


class MountainManager:

    def __init__(self) -> None:
        """
        Initialise the MountainManager.

        Complexity
        - Worst case: O(1), initialisation operation is a constant time operation.
        - Best case: O(1), same as worst case

        """
        self.mountains = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain):
        """
        Add a mountain to the manager.

        Complexity
        - Worst case: O(1), __setitem__ operation is a constant time operation.
        - Best case: O(1), same as worst case

        """
        #  key1: difficulty level, key2: name, value: mountain
        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain):
        """
        Remove a mountain from the manager.

        Complexity
        - Worst case: O(1), deletion operation is a constant time operation.
        - Best case: O(1), same as worst case

        """
        del self.mountains[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        Remove the old mountain and add the new mountain.

        Complexity
        - Worst case: O(1), remove and add operation are both constant time operations.
        - Best case: O(1), same as worst case

        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        """
        Return a list of all mountains with this difficulty.

        Complexity
        - Worst case: O(N), where N is the number of mountains in the hash table.
        - Best case: O(1), when the first key checked matches the given difficulty level,
          or when the hash table is empty.

        """
        # get all keys from hash table
        keys_list = self.mountains.keys()

        for key in keys_list:
            # if key matches corresponding difficulty, return value
            if int(key) == diff:
                return self.mountains.values(key)

        return []  # return empty list if no mountains with diff is found

    def group_by_difficulty(self):
        """
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.

        Complexity
        - Worst case: O(N log(N)), where N is the number of mountains in the hash table.
        - Best case: O(N), when the keys in the hash table are already sorted.

        """
        # get all keys from hash table
        keys_list = self.mountains.keys()
        sorted_values = []

        # Sort the keys using mergesort
        for key in mergesort(keys_list):

            # Get the values for the current key and append them to the sorted_values list
            current_values = self.mountains.values(key)
            sorted_values.append(current_values)

        return sorted_values
