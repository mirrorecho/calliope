import abjad
import calliope
import uqbar

class MachineSelectableMixin(object):

    # @property
    # def select_universe(self):
    #     return self

    def get_nodes(self):
        # TO DO... delay creating the list?
        my_nodes = [self]
        my_nodes.extend(self.depth_first())
        return my_nodes

    @property
    def nodes(self):
        return Selection(
            select_from=self.get_nodes()
            )        

    def by_type(self, *args):
        return Selection(
            select_from=self.get_nodes(), 
            type_args=args
            )

    # TO CONSIDER
    # able to set pitches / rhythm at this level (as opposed to machine)

    # TO CONSIDER
    # @property
    # def beats(self):
    #     return self._beats

    # @property
    # def measures(self):
    #     return None

    @property
    def phrases(self):
        return self.by_type(calliope.Phrase)

    @property
    def select(self):
        return Selection(select_from=self.children)

    @property
    def select_cells(self):
        return Selection(select_from=self.children, type_args=(calliope.Cell,))

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
    def logical_ties(self):
        return self.by_type(calliope.LogicalTie)

    @property
    def logical_ties_or_container(self):
        return self.by_type(calliope.LogicalTie, calliope.ContainerCell)

    # TO DO: not working yet... finish inplementing:
    # def tag_span(self, open_tag, close_tag=None):
    #     open_tag = list(self.spanner_closures[close_tag])[0]
    #     self[0].tag(open_tag)
    #     close_tag = 
    #     self[-1].tag()

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

    def __init__(self, select_from=(), select_root=None, *args, **kwargs):
        super().__init__()
        self.select_from = select_from
        self.select_root = select_root or getattr(select_from, "select_root", None)
        self.setup(**kwargs)

    def print_comments(self):
        my_len = len(self)
        return_str = "with %s items" % my_len + ": [\n"
        for i in self[:10]:
            return_str += "#    %s\n" % i
        if my_len > 10:
            return_str += "#    ... (%s more)\n" % (my_len-10)
        return_str += "#    ]"
        return return_str


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

    def exclude(self, *args, **kwargs):
        select_args = []
        for a in args:
            if isinstance(a, int) and a < 0:
                a = len(self) + a
            select_args.append(a)
        return ExcludeSelection(self, select_args=select_args, filter_kwargs=kwargs)

    # def reset_selection(self):
    #     self._length = None

    def insert(self, index, new_item):
        item = self[index]
        item.parent.insert(item.my_index, new_item) 

    # @property
    # def select_universe(self):
    #     # TO DO: is this right???
    #     for item in self:
    #         for child in item:
    #             yield child

    def get_nodes_generator(self):
        # TO DO... does this work OK????
        # TO DO... does this delay creating the list?
        for item in self:
            yield item
            for tree_node in item.depth_first():
                yield tree_node

    def get_nodes(self):
        return list(self.get_nodes_generator())

    def get_children_generator(self):
        for item in self:
            for tree_node in item.children:
                yield tree_node
    
    @property
    def children(self):
        return list(self.get_children_generator())

    def item_ok(self, index, item):
        
        if not (self.type_args or self.select_args or self.range_args or self.filter_kwargs):
            return True

        if self.type_args and isinstance(item, self.type_args):
            return True
        
        if self.select_args or self.range_args:
            if self.select_args: 
                if index in self.select_args or item.name in self.select_args:
                    return True
            if self.range_args:
                for r in self.range_args:
                    if index in r:
                        return True

        if self.filter_kwargs:
            for n, v in self.filter_kwargs.items():
                try:
                    if "__" in n:
                        n, pred = n.split("__")
                        if pred == "in" and getattr(item, n) in v:
                            return True
                        if pred == "lt" and getattr(item, n) < v:
                            return True
                        elif pred == "gt" and getattr(item, n) > v:
                            return True
                    elif getattr(item, n) == v:
                        return True
                except:
                    self.warn("tried to filter by '%s', but this attribute doesn't exist or invalid operator" % n)
        return False

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
        return list(self)

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


