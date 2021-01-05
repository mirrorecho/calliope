import sys, functools
import abjad, calliope
import inspect
import os

# GOALS:
# DONE: refer to content from other modules in a standard, convenient way
# DONE: prevent global loading of resource-intensive content unless needed
# DONE: create copies of content easily (and by default)

# EVENTUALLY
# illustrate all (with limit), or by category (also with limit)

# MAYBE:
# caching? (assume NO, because difficult to capture everything needed)


def register(func):
    """Register a function as a plug-in"""

    # TO DO... ????
    # def decorator_register(func):
    #     @functools.wraps(func)
    #     def wrapper_register():

    # print("I'm registering!", func)
    # print(lib)
    # lib.add(func)

    calling_info = inspect.stack()[1]
    my_module = inspect.getmodule(calling_info[0])

    # calling_module_file = calling_info[1]
    # calling_module_directory = os.path.dirname(calling_module_file)
    # calling_module_name = os.path.split(calling_module_file)[1].split(".")[0]
    # print(calling_module_name)

    # my_module = sys.modules[__name__]
    #
    if not hasattr(my_module, "_registered"):
        my_module._registered = {}
    #
    # # TO DO... this wonky...
    my_module._registered[func.__name__] = func
    return func


class Library(calliope.CalliopeBase):
    """
    A lazily-executed library of callables that generate musical content (calliope data structures).
    """
    _funcs = None
    _items = None
    _loaded = None  # a set of names of categories of things that have been loaded

    def is_loaded(self, name):
        return name in self._loaded

    def mark_loaded(self, name):
        self._loaded.add(name)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._funcs = {}
        self._items = {}
        self._loaded = set()

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            raise Exception("args length must be greater than 0")
        elif len(args) == 1:
            return self.get(args[0])(**kwargs)
        else:
            return [self.get(a)(**kwargs) for a in args]

    @property
    def names(self):
        return list(self._funcs.keys())

    def print_names(self, prefix=""):
        for name in self.names:
            if name.startswith(prefix):
                print(name)

    def get(self, arg):
        """ gets a single item """
        if arg not in self._items:
            self._items[arg] = self._funcs[arg](self)    
        return self._items[arg]

    def __getitem__(self, arg):
        if isinstance(arg, tuple):
            return [self.get(a) for a in arg]
        else:
            return self.get(arg)

    def __setitem__(self, name, value):
        """
        adds an item without waiting for lazy evaluation
        """
        self._items[name] = value
        self._funcs[name] = lambda: value  # for consistency

    def reload(self, *args):
        """
        reloads items (re-evaluates functions)
        """
        for n in self._funcs:
            if not args or n in args:
                self._items[n] = self._funcs[n]()

    def add(self, *args, namespace=None, category=None):
        """
        adds functions to be evaluated lazily when got by key from library
        """
        for func in args:
            my_name = func.__name__ if not namespace else namespace + "_" + func.__name__
            self._funcs[my_name] = func

    # TO DO... test... or delete KISS?!
    def add_selection_names(self, selection, *args, namespace=None):
        for my_name in args:
            if namespace:
                my_name = namespace + "_" + my_name
            self._funcs[my_name] = lambda: selection[my_name]

    def set_nodes(self, node, *args, namespace=None):
        """
        set child nodes by selection arguments
        (no lazy evaluation)
        """
        for select_attr in args:
            for n in getattr(node, select_attr):
                my_name = n.name
                if namespace:
                    my_name = namespace + "_" + my_name
                self[my_name] = n
