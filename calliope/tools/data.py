import collections
import abjad
from copy import copy, deepcopy

# d = {}
# b = None
# print( set(dir(d)) - set(dir(b)) )

# TO DO EVENTUALLY... look into abjad tree data structures (or other tree structures)... may be useful here instead of reinventing the wheel
class SetAttributeMixin(object):
    def __init__(self, **kwargs):
        super().__init__()
        for name, value in kwargs.items():
            setattr(self, name, value)

    # MAY NEED THESE????
    # def __str__(self):
    #     my_string = ""
    #     # TO DO... this is silly...
    #     class DummyClass(object):
    #         pass
    #     for a in sorted(set(dir(self)) - set(dir(DummyClass()))):
    #         my_string += a + "=" + str(getattr(self, a)) + " | "
    #     return my_string

    # def copy(self):
    #     return deepcopy(self) # deep copy probably not needed... but just to be safe...

class Tree(SetAttributeMixin, abjad.datastructuretools.TreeContainer):
    children_type = None

    # sometimes items are moved arround... this can be used track where an element had been placed previously, which is often useful
    original_index = None 
    original_depthwise_index = None # TO DO... consider making these IndexedData objects at the parent level?

    def index_children(self):
        for i, child in enumerate(self.children):
            child.original_index = i
            child.original_depthwise_index = child.depthwise_index # TO DO... this could get expensive

    @property
    def my_index(self):
        return self.parent.index(self)
        # return self.graph_order[-1] # NOTE... this does the same thing... which performs better??


    @property
    def depthwise_index(self):
        """
        Not sure how well this performs, but it works
        """
        return self.root.depthwise_inventory[self.depth].index(self)

    def copy(self):
        new_self = deepcopy(self)
        # for child in self.children:
        #     new_self.append(child.copy())
        return new_self

    def branch(self, **kwargs):
        new_branch = self.children_type(**kwargs)
        self.append( new_branch )
        return new_branch

    def __str__(self):
        my_return_string = self.__class__.__name__ + ":" + str(self.depthwise_index)
        if self.parent and self.parent is not self.root:
            my_return_string = str(self.parent) + " | " + my_return_string
        return my_return_string

class IndexedData(SetAttributeMixin, collections.UserDict):
    """
    behaves sort of like a cross between a list and a dictionary.
    """
    default = None
    min_limit=0
    limit=1
    cyclic = True
    cyclic_start=0
    over_limit_defaults=True # if False, then attempting to get by indices >= limit will throw an exception. (only applies if cyclic=False)
    items_type = object # WARNING, this must be defined at the class level

    # TO DO: implement this?
    # def keys(self):
    #     return collections.abc.KeysView(range(self.limit))


    def __init__(self, initialize_from=None, default=None, limit=None, **kwargs):
        super().__init__(**kwargs)
        self.default = default if default is not None else self.default
        self.limit = limit if limit is not None else self.limit
        if initialize_from:
            self.update(initialize_from)

    def get_default(self):
        if hasattr(self.default, "__call__"):
            return self.default()
        else:
            return self.default

    @classmethod
    def item(cls, **kwargs):
        return cls.items_type(**kwargs)

    # TO DO... + doesn't work right with multiple IndexedData objects (due to max methed in update)
    # TO DO... coerce items into a particular type?
    # TO DO... implement append, __mul__, insert, enumerate, items, make immutable?
    # TO DO... implement better slicing (e.g. slicing outside of limits)
    # TO DO... calling max... odd behavior (returns first item's value)... why?
    # TO DO?... force items type if defined? (i.e. throw exeption if type doesn't match?)

    # def __lt__(self, value, other):
    #     print(value)
    #     return value < other

    # NOTE: due to the iterable implementation, max(some_indexed_data) will return the max VALUE (not max key as a normal dictionary would),
    # so implementing this to get the max key
    def maxkey(self):
        if len(self.data) > 0:
            return max(self.data)

    def update(self, from_dict):
        if isinstance(from_dict, IndexedData):
            from_dict = from_dict.data
        for key in from_dict:
            assert isinstance(key, int), "key is not an integer: %s" % key
        # test for length 0, otherwise calling max on dict fails
        from_limit = 0 if len(from_dict) == 0 else max(from_dict)
        if self.limit <= from_limit:
            self.limit = from_limit + 1
        super().update(from_dict)

    def __iadd__(self, other):
        if isinstance(other,collections.UserDict) or isinstance(other,dict):
            self.update(other)
        elif isinstance(other, tuple) or isintance(other, list):
            self.extend(other)
        else:
            raise TypeError("Cannot add object of type %s to IndexedData object" % type(other))
        return self

    def copy(self):
        d = type(self)()
        # TO DO EVENTUALLY... could make this more elegant
        d.default = self.default
        d.min_limit=self.min_limit
        d.limit=self.limit
        d.cyclic = self.cyclic
        d.cyclic_start=self.cyclic_start
        d.over_limit_defaults=self.over_limit_defaults
        d += self
        return d

    def __add__(self, other):
        d = self.copy() 
        d += other
        return d

    def flattened(self):
        """
        if each item contains an iterable, this can create a combined, flattened list
        """
        # CONFUSING! see: http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        return [item for sublist in self for item in sublist] 

    def non_default_items(self):
        return sorted(self.data.items())

    def keylist(self):
        return sorted(list(self.data.keys()))

    def fillme(self, indices, value):
        if indices:
            if self.limit <= max(indices):
                self.limit = max(indices) + 1
            for i in indices:
                if hasattr(value, "__call__"):
                    # TO DO... better to call this over and over or set value once outside of loop?
                    self[i] = value()
                else:
                    self[i] = value
        else:
            print("WARNING: fillme with value '%s' will have no effect since no indices passed." % value)

    @classmethod
    def fill(cls, indices, value):
        me = cls()
        me.fillme(indices, value)
        return me

    def as_list(self):
        # TO DO: this is a little screwy and doesn't work for indices outside the limits or for min_limit !=0
        return [self[i] for i in range(self.limit) ]

    def extend(self, values):
        extend_from = 0
        if len(self.data) > 0:
            extend_from = max(self.data) + 1
        for i, v in enumerate(values):
            self[i+extend_from]=v

    def __setitem__(self, key, value):
        assert isinstance(key, int), "key is not an integer: %s" % key
        if hasattr(value, "__call__"):
            self.data[key] = value()
        else:
            self.data[key] = value
        if self.limit <=key:
            self.limit = key + 1

    def __len__(self):
        return self.limit

    def __getitem__(self, key):
        if isinstance(key, slice):
            # TO DO: this is a little screwy and doesn't work for indices outside the limits or for min_limit !=0
            return self.as_list()[key]
        if self.cyclic:
            if self.cyclic_start > 0 and (key >= self.cyclic_start or key < 0):
                if key > 0:
                    key = ( (key - self.cyclic_start) % (self.limit - self.cyclic_start) ) + self.cyclic_start
                else:
                    key = (key % (self.limit - self.cyclic_start)) + self.cyclic_start
            else:
                key = key % self.limit
        if key in self:
            return self.data[key]
        elif key < self.limit or self.over_limit_defaults:
            return self.get_default()
        else:
            raise KeyError(key)

    def __iter__(self):
        for x in range(self.min_limit, self.limit):
            yield self[x]

    def __str__(self):
        def str_line(key, value):
            key_len = len(str(key))
            spacing = " " * (8-key_len) if key_len<8 else ""
            return " |%s%s: %s\n" % (spacing, key, value)
        my_string = "<IndexedData object>\n"
        my_string += str_line("default", self.get_default())
        for key, value in self.non_default_items():
            if key < self.limit:
                my_string += str_line(key, value)
        my_string += str_line(self.limit, "MAX")
        return my_string

class ID1(IndexedData): # just to save typing, since this is used often
    cyclic_start = 1