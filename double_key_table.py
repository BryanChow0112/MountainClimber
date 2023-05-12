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
        self.size_index = 0
        self.table = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        self.internal_sizes = internal_sizes

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key1))
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

        :complexity: O(len(key2))
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

        Complexity
        :complexity best: O(hash1(key1)) first position is empty
        :complexity worst: O(hash1(key1) + N*comp(key1)) when we've searched the entire table
                        where N is the tablesize

        : raises KeyError:e When the key pair is not in the table, but is_insert is False.
        : raises FullError: When a table is full and cannot be inserted.
        """
        pos1 = self.hash1(key1)

        for _ in range(self.table_size):
            if self.table[pos1] is None:
                if is_insert:
                    linear_probe_table = LinearProbeTable(self.internal_sizes)
                    linear_probe_table.hash = lambda k : self.hash2(k, linear_probe_table)
                    self.table[pos1] = (key1, linear_probe_table)
                    pos2 = linear_probe_table._linear_probe(key2, is_insert)
                    self.count += 1
                    return pos1, pos2
                else:
                    raise KeyError("key pair is not in the table")
            elif self.table[pos1][0] == key1:
                linear_probe_table = self.table[pos1][1]
                pos2 = linear_probe_table._linear_probe(key2, is_insert)
                return pos1, pos2
            else:
                pos1 = (pos1 + 1) % self.table_size

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

        Complexity:
        - Best case: O(1) - when the table is empty or the specified key doesn't exist in the table.
        - Worst case: O(n * m) - when key is None,all positions are occupied where n is self.table_size and m is
        linear_probe_table.table_size.
        """
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

        Complexity:
        - Best case: O(1) - when the table is empty or the specified key doesn't exist in the table.
        - Worst case: O(n * m) - when key is None,all positions are occupied where n is self.table_size and m is
        linear_probe_table.table_size.
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

        Complexity:
        - Best case: O(1) - when the table is empty or the specified key doesn't exist in the table.
        - Worst case: O(n * m) - when key is None,all positions are occupied where n is self.table_size and m is
        linear_probe_table.table_size.
        """
        if key is None:
            for x in range(self.table_size):
                if self.table[x] is not None:
                    linear_probe_table = self.table[x][1]
                    for y in range(linear_probe_table.table_size):
                        if linear_probe_table.array[y] is not None:
                            yield linear_probe_table.array[y][1]
        else:
            pos1 = self.hash1(key)
            linear_probe_table = self.table[pos1][1]
            for y in range(linear_probe_table.table_size):
                if linear_probe_table.array[y] is not None:
                    yield linear_probe_table.array[y][1]
 

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Complexity:
        - Best case: O(1) - when the table is empty or the specified key doesn't exist in the table.
        - Worst case: O(n * m) - when key is None,all positions are occupied where n is self.table_size and m is
        linear_probe_table.table_size.
            """
        res: list = []
        if key is None:
            for x in range(self.table_size):
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

        :complexity: See linear probe.
        :raises KeyError: when the key doesn't exist.
        """
        key1, key2 = key
        int1, int2 = self._linear_probe(key1, key2, False)
        return self.table[int1][1][int2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :complexity: See linear probe.
        """
        key1, key2 = key
        pos1, pos2 = self._linear_probe(key1, key2, True)

        self.table[pos1][1][key2] = data

        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :complexity best: O(hash1(key1)) deleting item is not probed and in correct spot.
        :complexity worst: O(N*hash1(key1)+N^2*comp(key1)) deleting item is midway through large chain.
        :raises KeyError: when the key doesn't exist.
        """
        key1, key2 = key
        int1, int2 = self._linear_probe(key1, key2, False)
        # Remove the element
        if len(self.table[int1][1]) == 1:
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

            linear_probe_table = self.table[int1][1]
            linear_probe_table.__delitem__(key2)


    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash1(key1)) No probing.
        :complexity worst: O(N*hash1(key1) + N^2*comp(key1)) Lots of probing.
        Where N is len(self)
        """
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
                        self[key1, key2] = value
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        complexity: O(1)
        """
        return len(self.table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        complexity: O(1)
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
