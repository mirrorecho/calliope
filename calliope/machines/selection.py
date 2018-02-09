import abjad
import calliope

class MachineSelectableMixin(object):

    @property
    def select_universe(self):
        return self

    def by_type_universe(self, tree_universe):
        # return [t for t in getattr(self, tree_universe)]
        # for tree_node in getattr(self, tree_universe):
        #     yield tree_node
        return getattr(self, tree_universe)

    def by_type(self, *args, tree_universe="nodes"):
        # self.info( ("calling by type", args) )
        return Selection(
            select_from=self.by_type_universe(tree_universe), 
            type_args=args
            )

    @property
    def select(self):
        return Selection(self.select_universe)    

    @property
    def phrases(self):
        return self.by_type(calliope.Phrase)

    @property
    def cells(self):
        return self.by_type(calliope.Cell)

    @property
    def events(self):
        return self.by_type(calliope.Event)

    @property
    def non_rest_events(self):
        return self.by_type(calliope.Event).exclude(rest=True)

    @property
    # TO DO... consider... would this perform better by returning a selection leaves instead of 
    # selecting by type?
    def logical_ties(self):
        return self.by_type(calliope.LogicalTie)

    # TO DO... CONSIDER THIS FOR 'ABSTRACT' SELECTIONS
    # not currently working...
    def select_with(self, selection):
        selection.innermost_selection.select_from = self
        return selection


class Selection(MachineSelectableMixin, calliope.CalliopeBaseMixin):
    select_from = ()
    select_args = None # iterable of names or indices of items
    filter_kwargs = None # dictionary of attribute names/values to match
    range_args = None # iterable of ranges of indices
    type_args = None # iterable of types to match

    # _length = None # cached length?

    def __init__(self, select_from=(), *args, **kwargs):
        super().__init__()
        self.select_from = select_from
        self.setup(**kwargs)

    # TO DO... consider if useful:
    # @property
    # def innermost_selection(self):
    #     if isinstance(self.select_from, Selection):
    #         return self.select_from.innermost_selection
    #     else:
    #         return self

    def cache(self):
        # TO DO: implement cache?
        self.warn("cache method not implemented yet")
        pass

    def exclude(self, *args, **kwargs):
        select_args = []
        for a in args:
            if isinstance(a, int) and a < 0:
                a = len(self) + a
            select_args.append(a)
        return ExcludeSelection(self, select_args=select_args, filter_kwargs=kwargs)

    # def reset_selection(self):
    #     self._length = None

    @property
    def select_universe(self):
        # TO DO: is this right???
        for item in self:
            for child in item:
                yield child

    def by_type_universe(self, tree_universe):
        # TO DO... does this work OK????
        print("SYO")
        for item in self:
            for tree_node in getattr(item, tree_universe):
                yield tree_node

    def item_ok(self, index, item):
        
        if self.type_args and not isinstance(item, self.type_args):
            return False

        # self.info(type(item))
        
        if self.select_args or self.range_args:
            arg_found = False
            if self.select_args: 
                if index in self.select_args or item.name in self.select_args:
                    arg_found = True
                    # item.info("FOUND")
            if not arg_found and self.range_args:
                # print(self.range_args[0])
                # print("HAHAHAHA")
                for r in self.range_args:
                    if index in r:
                        arg_found = True
                        break
            if not arg_found:
                return False

        if self.filter_kwargs:
            for n, v in self.filter_kwargs.items():
                try:
                    if n[-4:] == "__in":
                        return getattr(item, n[:-4]) in v
                    if n[-4:] == "__lt":
                        return getattr(item, n[:-4]) < v
                    elif n[-4:] == "__gt":
                        return getattr(item, n[:-4]) > v
                    elif getattr(item, n) != v:
                        return False
                except:
                    self.warn("tried to filter by '%s', but this attribute doesn't exist or invalid operator" % n)
                    return False
        return True

    def __getitem__(self, arg):
        
        def get_index(num):
            """
            returns actual positive index for negative indexes, based on selection length
            """
            return len(self) + num if num < 0 else num

        try:
            def get_range(my_slice):
                range_start = my_slice.start
                if range_start is None:
                    range_start = 0
                range_stop = my_slice.stop
                if range_stop is None:
                    range_stop = len(self)
                range_step = my_slice.step or 1
                if range_step < 0:
                    self.warn("Slicing with negative step not supported... beware of unexpected results! Use reversed() instead.")
                return range(get_index(range_start), get_index(range_stop), range_step)

            if isinstance(arg, int):
                my_index = get_index(arg)
                return next(x for i, x in enumerate(self) if i==my_index)
            elif isinstance(arg, str):
                return next(x for x in self if x.name==arg)
            if isinstance(arg, slice):
                return Selection(self, range_args=(get_range(arg),) )
            if isinstance(arg, tuple):
                select_args = []
                range_args = []
                for a in arg:
                    if isinstance(a, slice):
                        range_args.append( get_range(a) )
                    else:
                        if isinstance(a, int):
                            a = get_index(a)
                        select_args.append(a)
                return Selection(self, select_args=select_args, range_args=range_args)
        except StopIteration as ex:
            raise KeyError("%s not in selection" % arg) from ex

    @property            
    def as_reversed(self):
        return Selection( reversed(self) )

    def tag(self, *args):
        for item in self:
            item.tag(*args)

    def untag(self, *args):
        for item in self:
            item.untag(*args)

    def apply(self, func):
        # TO DO... test... works OK?
        map(func, self)        

    def setattrs(self, **kwargs):
        for item in self:
            for n, v in kwargs.items():
                setattr(item, n, v)

    def fuse(self):
        self.warn("fuse is not implemented yet!")

    def split_rhythm(self, *args, **kwargs):
        self.warn("split_rhythm is not implemented yet!")

    def copy(self, *args, **kwargs):
        return Selection([item(*args, **kwargs) for item in self])

    def copy_tree(self, with_rests=False, *args, **kwargs):
        self.warn("copy_tree is not implemented yet!")

    def as_list(self):
        return [x for x in self]

    def __iter__(self):
        # self.info("calling iter")
        # for x in self.get_selection():
        #     yield x
        for i,u in enumerate(self.select_from):
            # self.info( (i, self.item_ok(i,u), type(u)) )
            if self.item_ok(i,u):
                yield u
            # else:
                # self.info( (i, "--") )

    def __len__(self):
        # self._length = self._length or sum(1 for x in self)
        # return self._length
        return sum(1 for x in self)

    def __call__(self, *args, **kwargs):
        return Selection(self, select_args=args, filter_kwargs=kwargs)

class ExcludeSelection(Selection):
    def item_ok(self, index, item):
        return not(super().item_ok(index, item))


