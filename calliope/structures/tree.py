import inspect
import copy
import abjad
from calliope import tools

class TreeMixin(object):
    pass

class Tree(TreeMixin, abjad.datastructuretools.TreeContainer):
    child_types = ()

    # TO DO: use these...?
    # sometimes items are moved arround... this can be used track where an element had been placed previously, which is often useful
    original_index = None 
    original_depthwise_index = None # TO DO... consider making these IndexedData objects at the parent level?

    def _init_append_children(self):
        for node_name in type(self).class_sequence(): 
            # TO DO: WARNING: this won't work for class-based nodes... implement for classes?
            node = getattr(self, node_name)
            self[node_name] = node


    def __init__(self, *args, **kwargs):

        children = args
        super().__init__(children)

        name = kwargs.pop("name", None)
        if name:
            self.name = name

        if not self.child_types:
            self.child_types = (Tree,)

        for name, value in kwargs.items():
            setattr(self, name, value)

        self._init_append_children()


    # TO DO... screwy?
    def __call__(self, name=None, **kwargs):
        return_node = copy.deepcopy(self)
        if name:
            return_node.name = name
        for name, value in kwargs.items():
            setattr(return_node, name, value)
        return return_node

    def __setitem__(self, arg, node):
        if inspect.isclass(node):
            node = node()
        if type(arg) is slice:
            # needed for base TreeContainer implementation:
            abjad.datastructuretools.TreeContainer.__setitem__(self, arg, node)
        elif not isinstance(node, self.child_types):
            # print(self.child_types)
            # print(node)
            self.warn("attempted to add child but not an allowed child type - attribute/child not added", node)
        else:
            if type(arg) is int:
                # if setting based on integer index or slice, use abjad's tree container default behavior
                abjad.datastructuretools.TreeContainer.__setitem__(self, arg, node)
            else:
                node.name = arg # just as a precaution
                
                # TO DO... assume we don't want to deal with this... but consider it
                # setattr(self, arg, node)
                new_child = True

                for i, b in enumerate(self.children):
                    if b.name == arg:
                        abjad.datastructuretools.TreeContainer.__setitem__(self, i, node)
                        new_child = False
                        break
                if new_child:
                    abjad.datastructuretools.TreeContainer.__setitem__(self,
                        slice(len(self), len(self)),
                        [node]
                        )


    @classmethod
    def class_sequence(cls, child_types=(), **kwargs):
        my_sequence = []

        # # This adds all tree classes to the sequence, in the defined order:
        class_hierarchy = inspect.getmro(cls)[::-1]
        child_types = child_types or cls.child_types or (Tree, )

        for c in class_hierarchy:
            if issubclass(c, TreeMixin):
                for name, attr in c.__dict__.items():
                    if inspect.isclass(attr) and issubclass(attr, child_types) and not name in my_sequence:
                        my_sequence.append(name)
                    elif isinstance(attr, child_types):
                        my_sequence.append(name)
        return my_sequence

    # TO DO: even necessary anymore?
    def sequence(self, **kwargs):
        return [b.name for b in self.children]

    def by_type(self, *args):
        return [e for e in self.nodes if isinstance(e, args) ]

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

    # TO DO... is this every used?
    def copy(self):
        return copy.deepcopy(self)
        # for child in self.children:
        #     new_self.append(child.copy())

    # TO DO... used? depreciate?
    def index_children(self):
        for i, child in enumerate(self.children):
            child.original_index = i
            child.original_depthwise_index = child.depthwise_index # TO DO... this could get expensive

    def warn(self, msg, data=None, **kwargs):
        print("WARNING - %s: %s" % (self.__class__.__name__, msg)  )
        if data is not None:
            print(data)
        print("------------------------------")

    def info(self, msg, data=None, **kwargs):
        print("INFO - %s: %s" % (self.__class__.__name__, msg)  )
        if data is not None:
            print(data)
        print("------------------------------")

    def verify(self, condition, msg=None, data=None, **kwargs):
        if not condition:
            self.warn(msg or "(no message)", data)
        return condition



#     # sometimes items are moved arround... this can be used track where an element had been placed previously, which is often useful
#     original_index = None 
#     original_depthwise_index = None # TO DO... consider making these IndexedData objects at the parent level?

#     def __init__(self, *args, **kwargs):
#         super().__init__(**kwargs)
#         if not self.child_types:
#             self.child_types = (self.__class__,)

#     def index_children(self):
#         for i, child in enumerate(self.children):
#             child.original_index = i
#             child.original_depthwise_index = child.depthwise_index # TO DO... this could get expensive

#     # TO DO... is this every used?
#     def copy(self):
#         new_self = deepcopy(self)
#         # for child in self.children:
#         #     new_self.append(child.copy())
#         return new_self

#     def __str__(self):
#         my_return_string = self.__class__.__name__ + ":" + str(self.depthwise_index)
#         if self.parent and self.parent is not self.root:
#             my_return_string = str(self.parent) + " | " + my_return_string
#         return my_return_string
