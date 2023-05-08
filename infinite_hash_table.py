from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise, `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.level = level
        self.array = ArrayR(self.TABLE_SIZE)
        self.count = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        # get the index in the array where the (key, value) pair would be stored
        index = self.hash(key)

        # if position is empty (item not exist)
        if self.array[index] is None:
            raise KeyError(key)

        # if position contains hash table, recursively get the value
        elif isinstance(self.array[index][1], InfiniteHashTable):
            return self.array[index][1][key]

        # if the value at position is not an InfiniteHashTable and is not None, return it
        elif self.array[index][1] is not None:
            return self.array[index][1]

        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set a (key, value) pair in our hash table.
        """
        # get the index in the array where the (key, value) pair would be stored
        index = self.hash(key)

        # If the position is empty, set the key-value pair directly
        if self.array[index] is None:
            self.array[index] = (key, value)
            self.count += 1

        # If there's a sub-table, recurse to set the key in the sub-table
        elif isinstance(self.array[index][1], InfiniteHashTable):
            self.array[index][1][key] = value
            self.count += 1

        else:
            # If there's a collision, create a new sub-table and re-insert the existing key-value pair and the new one
            sub_table = InfiniteHashTable(self.level + 1)

            existing_key, existing_value = self.array[index]

            sub_table[existing_key] = existing_value
            sub_table[key] = value

            self.array[index] = (existing_key[:self.level + 1], sub_table)
            self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        # get the index in the array where the (key, value) pair would be stored
        index = self.hash(key)

        if self.array[index] is not None:

            # If the value at index is an internal hash table, recursively call __delitem__ on it
            if isinstance(self.array[index][1], InfiniteHashTable):

                del self.array[index][1][key]
                self.count -= 1

                # If the internal hash table now only contains a single item, replace the hash table with that item
                if len(self.array[index][1]) == 1:

                    for i in range(self.array[index][1].TABLE_SIZE):
                        if self.array[index][1].array[i] is not None:

                            # Extract the key-value pair from the internal hash table
                            sub_key, sub_value = self.array[index][1].array[i]

                            # Replace the internal hash table with the extracted key-value pair
                            self.array[index] = (sub_key, sub_value)

                            break

            else:
                # If there's no internal hash table, remove the key-value pair from the array
                self.array[index] = None
                self.count -= 1

        else:
            raise KeyError(f"KeyError: {key}")

    def __len__(self):
        """
        Returns the number of (key, value) pairs in the hash table.
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        print()
        for i in range(len(self.array)):
            print(f"{i}", self.array[i])

        return ""

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        # get the index in the array where the (key, value) pair would be stored
        index = self.hash(key)

        # position is empty
        if self.array[index] is None:
            raise KeyError(f"Key {key} not found")

        # If there's a sub-table, recurse to get the sequence of positions
        elif isinstance(self.array[index][1], InfiniteHashTable):
            return [index] + self.array[index][1].get_location(key)

        # Item found (reached end)
        elif self.array[index][0] == key:
            return [index]

        else:
            raise KeyError(f"Key {key} not found")

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True