from mountain import Mountain
from double_key_table import DoubleKeyTable
from algorithms.mergesort import mergesort


class MountainManager:

    def __init__(self) -> None:
        self.mountains = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain):
        #  key1: difficulty level, key2: name, value: mountain
        self.mountains[str(mountain.difficulty_level), mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain):
        del self.mountains[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        # get all keys from hash table
        keys_list = self.mountains.keys()

        for key in keys_list:
            # if key matches corresponding difficulty, return value
            if int(key) == diff:
                return self.mountains.values(key)

        return []  # return empty list if no mountains with diff is found

    def group_by_difficulty(self):
        # get all keys from hash table
        keys_list = self.mountains.keys()
        sorted_values = []

        # Sort the keys using mergesort
        for key in mergesort(keys_list):

            # Get the values for the current key and append them to the sorted_values list
            current_values = self.mountains.values(key)
            sorted_values.append(current_values)

        return sorted_values
