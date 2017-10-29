import abjad
import calliope


# JUST FOR TESTING
# from closely.mark_d import material_d

class MachineSelectableMixin(object):

    def select_universe(self):
        return self


    def by_type_universe(self, tree_universe):
        # return [t for t in getattr(self, tree_universe)]
        # for tree_node in getattr(self, tree_universe):
        #     yield tree_node
        return getattr(self, tree_universe)

    def by_type(self, *args, tree_universe="nodes"):
        self.info( ("calling by type", args) )
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
    # TO DO... THIS NEEDS TO RETURN A SELECTION, NOT A LIST
    def non_rest_events(self):
        return [e for e in self.events if not e.rest]

    @property
    # TO DO... THIS NEEDS TO RETURN A SELECTION
    def logical_ties(self):
        return self.leaves 
    # TO CONSIDER: better to select leaves or select by type=LogicalTie???

class Selection(MachineSelectableMixin, calliope.CalliopeBaseMixin):
    select_from = ()
    filter_kwargs = None
    type_args = None

    def __init__(self, select_from, *args, **kwargs):
        super().__init__()
        self.select_from = select_from
        self.setup(**kwargs)

    def select_universe(self):
        # TO DO: is this right???
        for item in self:
            for child in item:
                yield child

    def by_type_universe(self, tree_universe):
        PRINT("SYO")
        for item in self:
            for tree_node in getattr(item, tree_universe):
                yield tree_node

    def item_ok(self, index, item):
        if self.type_args and not isinstance(item, self.type_args):
            return False
        if self.filter_kwargs:
            for n, v in self.filter_kwargs.items():
                try:
                    if getattr(item, n) != v:
                        return False
                except:
                    self.warn("tried to filter by '%s', but this atribute doesn't exit" %s)
                    return False
        return True

    # def get_selection(self):
    #     # self.info("getting selection")
    #     return [u for i,u in enumerate(self.select_from) if self.item_ok(i,u)]

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return next(x for i, x in enumerate(self) if i==arg)
        elif isinstance(arg, str):
            return next(x for x in self if x.name==arg)
        if isinstance(arg, slice):
            return MultiSelection(self, select_args=(arg,))
        if isinstance(arg, tuple):
            return MultiSelection(self, select_args=arg)

    def tag(self, *args):
        for item in self:
            item.tag(*args)

    def apply(self, func):
        # TO DO... test... works OK?
        map(func, self)        

    def setattrs(self, **kwargs):
        for item in self:
            for n, v in kwargs.items:
                setattr(self, n, v)

    def fuse(self):
        self.warn("fuse is not implemented yet!")

    def split_rhythm(self, *args, **kwargs):
        self.warn("split_rhythm is not implemented yet!")

    def copy(self, *args, **kwargs):
        return [item(*args, **kwargs) for item in self]

    def copy_tree(self, with_rests=False, *args, **kwargs):
        self.warn("copy_tree is not implemented yet!")

    def __iter__(self):
        self.info("calling iter")
        # for x in self.get_selection():
        #     yield x
        for i,u in enumerate(self.select_from):
            if self.item_ok(i,u):
                # self.info( (i,"OK") )
                yield u
            # else:
                # self.info( (i, "--") )

    def __len__(self):
        return sum(1 for x in self)

    def __call__(self, *args, **kwargs):
        self.filter_kwargs = {**(self.filter_kwargs or {}),  **kwargs}
        if self.args:
            return MultiSelection(self, select_args=args)
        return self

class MultiSelection(Selection):
    select_args = () # indices, names, or slices

    def get_selection(self):
        self.info("getting multi selection")
        selected_list = []
        for arg in self.select_args:
            if isinstance(arg, int):
                selected_list.append(self.select_from[arg])
            elif isinstance(arg, str): 
                selected_list.append(next(x for x in self.select_from if x.name==arg))
            elif isinstance(arg, slice):
                selected_list.extend(self.select_from[arg])
        return selected_list

    def __call__(self, *args, **kwargs):
        self.select_args += args
        if kwargs:
            return Selection(self, filter_kwargs=kwargs)    
        return self


# class SubSelection(MachineSelectableMixin, calliope.CalliopeBaseMixin):
    

# class StarTest(MachineSelectableMixin, material_d.DStarI):
#     pass

# s = StarTest(name="STAR ME")
# s.phrases[0].cells.tag("ff")
# s.phrases[0].non_rest_events.tag("-", ">")
# calliope.illustrate_me(bubble=s)


