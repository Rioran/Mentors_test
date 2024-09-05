from bisect import bisect_left, insort
from collections import namedtuple
from doctest import testmod
from functools import lru_cache


HASH_LIMIT = 1028
DataPair = namedtuple('DataPair', ['key', 'value', 'order'])


class MyDict:
    def __init__(self):
        self._hash_space: list[None | list] = [None] * HASH_LIMIT
        self._active_hashes = set()
        self._keys = set()
        self._order_index = 0

    def __getitem__(self, key):
        """
        >>> my_dict = MyDict()
        >>> my_dict['name'] = 'Alice'
        >>> my_dict['name']
        'Alice'
        >>> my_dict['age'] = 30
        >>> my_dict['age'] = 33
        >>> my_dict['age']
        33
        >>> my_dict['non existant key']

        """
        if key not in self._keys:
            return None

        value_space = self._get_value_space(key)
        value_index = self._get_space_index_by_key(value_space, key)
        pair: DataPair = value_space[value_index]
        return pair.value

    def __setitem__(self, key, value):
        """
        >>> my_dict = MyDict()
        >>> my_dict['name'] = 'Alice'
        >>> my_dict['age'] = 30
        >>> my_dict['age'] = 33
        >>> my_dict[(1, 2, 3)] = (1, 2, 3)
        >>> my_dict[[1, 2, 3]] = 123
        Traceback (most recent call last):
        TypeError: unhashable type: 'list'
        """
        key_hash: int = self._get_hash_by_key(key)
        self._active_hashes.add(key_hash)

        value_space = self._get_value_space(key)

        if value_space is None:
            self._hash_space[key_hash] = value_space = list()

        if key in self._keys:
            value_space_index = self._get_space_index_by_key(value_space, key)
            old_key_value_pair = value_space[value_space_index]
            key_value_pair = DataPair(key, value, old_key_value_pair.order)
            value_space[value_space_index] = key_value_pair
        else:
            key_value_pair = DataPair(key, value, self._order_index)
            self._order_index += 1
            insort(value_space, key_value_pair, key=lambda pair: pair.key)

        self._keys.add(key)

    def __delitem__(self, key):
        """
        >>> my_dict = MyDict()
        >>> my_dict['name'] = 'Alice'
        >>> my_dict['name']
        'Alice'
        >>> del my_dict['name']
        >>> my_dict['name']
        >>> del my_dict['name']
        >>> my_dict['name']
        >>> del my_dict[[1, 2, 3]]
        Traceback (most recent call last):
        TypeError: unhashable type: 'list'
        """
        if key not in self._keys:
            return

        value_space: list = self._get_value_space(key)
        value_space_index = self._get_space_index_by_key(value_space, key)
        value_space.pop(value_space_index)

        if not value_space:
            key_hash = self._get_hash_by_key(key)
            self._active_hashes.discard(key_hash)

        self._keys.discard(key)

    @staticmethod
    @lru_cache
    def _get_hash_by_key(key) -> int:
        hash_value: int = hash(key)  # TypeError if not hashable
        hash_limited: int = hash_value % HASH_LIMIT
        return hash_limited

    def _get_value_space(self, key) -> list | None:
        key_hash = self._get_hash_by_key(key)
        value_space = self._hash_space[key_hash]
        return value_space

    @staticmethod
    def _get_space_index_by_key(value_space, value_key) -> int:
        index = bisect_left(value_space, value_key, key=lambda pair: pair.key)
        return index

    def _get_all_items_sorted(self) -> list[DataPair]:
        all_value_spaces = [
            self._hash_space[hash_index]
            for hash_index in self._active_hashes
        ]
        all_items = sum(all_value_spaces, start=list())
        all_items_sorted = sorted(all_items, key=lambda pair: pair.order)
        return all_items_sorted

    def keys(self):
        """
        >>> my_dict = MyDict()
        >>> my_dict[1], my_dict[3], my_dict[2] = 'one', 'three', 'two'
        >>> my_dict.keys()
        [1, 3, 2]
        """
        items = self._get_all_items_sorted()
        result = [item.key for item in items]
        return result

    def values(self):
        """
        >>> my_dict = MyDict()
        >>> my_dict[1], my_dict[3], my_dict[2] = 'one', 'three', 'two'
        >>> my_dict.values()
        ['one', 'three', 'two']
        """
        items = self._get_all_items_sorted()
        result = [item.value for item in items]
        return result

    def items(self):
        """
        >>> my_dict = MyDict()
        >>> my_dict[1], my_dict[3], my_dict[2] = 'one', 'three', 'two'
        >>> my_dict.items()
        [(1, 'one'), (3, 'three'), (2, 'two')]
        """
        items = self._get_all_items_sorted()
        result = [(item.key, item.value) for item in items]
        return result

    def __contains__(self, item):
        """
        >>> my_dict = MyDict()
        >>> my_dict['age'] = 30
        >>> print('age' in my_dict)
        True
        >>> print('city' in my_dict)
        False
        """
        return item in self._keys

    def __str__(self):
        """
        >>> my_dict = MyDict()
        >>> my_dict[1], my_dict[3], my_dict[2] = 'one', 'three', 'two'
        >>> str(my_dict)
        "[(1, 'one'), (3, 'three'), (2, 'two')]"
        """
        return str(self.items())


if __name__ == '__main__':
    testmod(verbose=True)
