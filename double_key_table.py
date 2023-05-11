from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        Initialise the DoubleKeyTable.

        Complexity
        - Worst case: O(1), initialisation operation is a constant time operation.
        - Best case: O(1), same as worst case

        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        if internal_sizes is not None:
            LinearProbeTable.TABLE_SIZES = internal_sizes
        self.size_index = 0
        self.table = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        : raises KeyError:e When the key pair is not in the table, but is_insert is False.
        : raises FullError: When a table is full and cannot be inserted.
        """
        pos1 = self.hash1(key1)
        int1: int = None
        for _ in range(len(self.table)):
            if self.table[pos1] is None:
                if is_insert:
                    int1 = pos1
                    linear_probe_table = LinearProbeTable()
                    int2 = self.hash2(key2, linear_probe_table)
                    return int1, int2
                else:
                    raise KeyError("key pair is not in the table")
            elif self.table[pos1][0] == key1:
                linear_probe_table = self.table[pos1][1]
                pos2 = self.hash2(key2, linear_probe_table)
                for x in range(self.table[pos1][1].table_size):
                    if self.table[pos1][1].array[pos2] is None:
                        if is_insert:
                            return pos1, pos2
                        else:
                            raise KeyError("key pair is not in the table")
                    elif self.table[pos1][1].array[pos2][0] == key2:
                        return pos1, pos2
                    else:
                        pos2 = (pos2 + 1) % self.table[pos1][1].table_size
            else:
                pos1 = (pos1 + 1) % len(self.table)
        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError("key pair is not in the table")

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        # res: list = []
        if key is None:
            for x in range(self.table_size):
                if self.table[x] is not None:
                    yield self.table[x][0]
        else:
            for x in range(self.table_size):
                if self.table[x] is not None:
                    if self.table[x][0] == key:
                        linear_probe_table = self.table[x][1]
                        for y in range(linear_probe_table.table_size):
                            if linear_probe_table.array[y] is not None:
                                yield linear_probe_table.array[y][0]

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        res: list = []
        if key is None:
            for x in range(self.table_size):
                if self.table[x] is not None:
                    res.append(self.table[x][0])
        else:
            for x in range(self.table_size):
                if self.table[x] is not None:
                    if self.table[x][0] == key:
                        linear_probe_table = self.table[x][1]
                        return linear_probe_table.keys()
        return res

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        if key is None:
            for x in range(len(self.table)):
                if self.table[x] is not None:
                    linear_probe_table = self.table[x][1]
                    for y in range(linear_probe_table.table_size):
                        if linear_probe_table.array[y] is not None:
                            yield linear_probe_table.array[y][1]
        else:
            pos1 = self.hash1(key)
            linear_probe_table = self.table[pos1][1]
            # return linear_probe_table.values()
            for y in range(linear_probe_table.table_size):
                if linear_probe_table.array[y] is not None:
                    yield linear_probe_table.array[y][1]
 

    def values(self, key: K1 | None = None) -> list[V]:
        """
            key = None: returns all values in the table.
            key = x: returns all values for top-level key x.
            """
        res: list = []
        if key is None:
            for x in range(len(self.table)):
                if self.table[x] is not None:
                    linear_probe_table = self.table[x][1]
                    for y in range(linear_probe_table.table_size):
                        if linear_probe_table.array[y] is not None:
                            res.append(linear_probe_table.array[y][1])
        else:
            pos1 = self.hash1(key)
            linear_probe_table = self.table[pos1][1]
            return linear_probe_table.values()
        return res

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        key1, key2 = key
        int1, int2 = self._linear_probe(key1, key2, False)
        return self.table[int1][1].array[int2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        key1, key2 = key
        int1, int2 = self._linear_probe(key1, key2, True)

        if self.table[int1] is None:
            self.count += 1
            linear_probe_table = LinearProbeTable()
            linear_probe_table.array[int2] = (key2, data)
            linear_probe_table.count += 1
            self.table[int1] = (key1, linear_probe_table)
        else:
            linear_probe_table = self.table[int1][1]
            linear_probe_table.array[int2] = (key2, data)
            linear_probe_table.count += 1

        if len(linear_probe_table) > linear_probe_table.table_size / 2 or len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        key1, key2 = key
        int1, int2 = self._linear_probe(key1, key2, False)
        # Remove the element
        if len(self.table[int1][1].keys()) == 1:
            self.table[int1] = None
            self.count -= 1
            int1 = (int1 + 1) % self.table_size
            while self.table[int1] is not None:
                key1_ = self.table[int1][0]
                key_, value_ = self.table[int1]
                self.table[int1] = None
                # Reinsert.
                int1_, int2_ = self._linear_probe(key1_, key_, True)
                # print(int1_)
                self.table[int1_] = (key_, value_)
                int1 = (int1 + 1) % self.table_size
        else:
            self.table[int1][1].array[int2] = None
            self.table[int1][1].count -= 1

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        if len(self) > self.table_size / 2:
            old_table = self.table
            self.size_index += 1
            if self.size_index == len(self.TABLE_SIZES):
                # Cannot be resized further.
                return
            self.table = ArrayR(self.TABLE_SIZES[self.size_index])
            self.count = 0
            for item in old_table:
                if item is not None:
                    key1, linear_probe_table = item
                    for y in range(linear_probe_table.table_size):
                        if linear_probe_table.array[y] is not None:
                            key2, value = linear_probe_table.array[y]
                            self[(key1, key2)] = value
        for x in range(self.table_size):
            if self.table[x] is not None:
                key1, linear_probe_table = self.table[x]
                # print(linear_probe_table)
                if len(linear_probe_table) > linear_probe_table.table_size / 2:
                    old_internal_table = linear_probe_table.array
                    linear_probe_table.size_index += 1
                    if linear_probe_table.size_index == len(linear_probe_table.TABLE_SIZES):
                        # Cannot be resized further.
                        return
                    linear_probe_table.array = ArrayR(linear_probe_table.TABLE_SIZES[linear_probe_table.size_index])
                    linear_probe_table.count = 0
                    for item in old_internal_table:
                        if item is not None:
                            key2, value = item
                            self[(key1, key2)] = value

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for external_table in self.table:
            if external_table is not None:
                (key1, internal_table) = external_table
                result += key1 + "\n" + str(internal_table)
        return result
