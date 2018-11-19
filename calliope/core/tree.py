import inspect
import copy
import abjad
import uqbar
import calliope

TREE_CONTAINER_MRO_COUNT = len(inspect.getmro(uqbar.containers.UniqueTreeContainer))

class SelectableMixin(calliope.BaseMixin):
    def get_nodes(self):
        # TO DO... delay creating the list?
        my_nodes = [self]
        my_nodes.extend(self.depth_first())
        return my_nodes

    @property
    def nodes(self):
        return calliope.Selection(
            select_from=self.get_nodes()
            )        

    def select_by_type(self, *args):
        return calliope.Selection(
            select_from=self.get_nodes(), 
            type_args=args
            )

    @property
    def select(self):
        return calliope.Selection(select_from=self.children)

    @classmethod
    def set_select_property(cls, name, select_type):
        setattr(cls, name, property(lambda x: x.select_by_type(select_type)))

    def print_comments(self):
        return "with %s children and %s nodes" % (len(self.children), len(list(self.depth_first()))+1)


class Tree(SelectableMixin, uqbar.containers.UniqueTreeContainer):
    child_types = ()
    select_property = None
    
    # # KISS!
    # parent_type = None 
    # original_index = None 
    # original_depthwise_index = None # TO DO... consider making these IndexedData objects at the parent level?


    # can be overriden to set children based on other/special logic
    # TO DO: consider merging with CopyChildrenBubble.set_children used in a couple places
    def set_children_from_class(self, *args, **kwargs):
        for node_name in type(self).class_sequence(): 
            node = getattr(self, node_name)
            self[node_name] = node

    def __init__(self, *args, **kwargs):
        # print(args)
        super().__init__(args) # TO DO... ??? WTF with args?
        self.setup(**kwargs)
        self.set_children_from_class(*args, **kwargs)
        if not self.child_types:
            self.child_types = (Tree,)


    def __call__(self, name=None, **kwargs):
        return_node = copy.deepcopy(self)
        if name:
            return_node.name = name # TO DO: ????
        for name, value in kwargs.items():
            setattr(return_node, name, value)
        return return_node

    def __setitem__(self, arg, node):
        if inspect.isclass(node):
            node = node()
        if type(arg) is slice:
            # needed for base UniqueTreeContainer implementation:
            uqbar.containers.UniqueTreeContainer.__setitem__(self, arg, node)
        elif not isinstance(node, self.child_types):
            # print(self.child_types)
            # print(node)
            self.warn("attempted to add child but not an allowed child type - attribute/child not added", node)
        else:
            if type(arg) is int:
                # if setting based on integer index or slice, use abjad's tree container default behavior
                uqbar.containers.UniqueTreeContainer.__setitem__(self, arg, node)
            else:
                node.name = arg # just as a precaution
                
                # TO DO... assume we don't want to deal with this... but consider it
                # setattr(self, arg, node)
                new_child = True

                for i, b in enumerate(self.children):
                    if b.name == arg:
                        uqbar.containers.UniqueTreeContainer.__setitem__(self, i, node)
                        new_child = False
                        break
                if new_child:
                    uqbar.containers.UniqueTreeContainer.__setitem__(self,
                        slice(len(self), len(self)),
                        [node]
                        )

    @classmethod
    def class_sequence(cls, child_types=() ):
        my_sequence = []
        # # This adds all tree classes to the sequence, in the defined order:
        for c in inspect.getmro(cls)[::-1][TREE_CONTAINER_MRO_COUNT:]:
            for name, attr in c.__dict__.items():
                if cls.is_child_type(attr, child_types) and not name in my_sequence:
                    my_sequence.append(name)
        return my_sequence

    @classmethod
    #DAH! Keep this? Too Hacky?
    def from_module(cls, module, **kwargs):
        module_members_info = sorted([
                (
                    inspect.getsourcefile(m[1]), 
                    inspect.getsourcelines(m[1])[1], 
                    m[0]
                ) if inspect.isclass(m[1])
                else 
                (
                    "z",
                    0,
                    m[0],
                )
                for m in inspect.getmembers(module, calliope.Tree.is_child_type)
            ])
        tree_node = cls(**kwargs)
        for c in module_members_info:
            child_name = c[2]
            child_node = module.__dict__[child_name]
            tree_node[child_name] = child_node
        return tree_node

    @classmethod
    def is_child_type(cls, obj, child_types=() ):
        child_types = child_types or cls.child_types or (Tree,)
        if isinstance(obj, child_types) or ( inspect.isclass(obj) and issubclass(obj, child_types) ):
            return True
        return False

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

    # TO DO... CONSIDER THIS FOR 'ABSTRACT' SELECTIONS
    # not currently working...
    def select_with(self, selection):
        selection.innermost_selection.select_from = self
        return selection


    # OK TO REMEVE?
    # def by_type(self, prototype):
    #     nodes = list(self.depth_first())
    #     return [e for e in nodes if isinstance(e, prototype) ]


    # KISS! 
    # def fuse(self, count):
    #     # TO DO... this could be more elegant!!!
    #     my_index = self.my_index
    #     for c in range(count):
    #         next_item = self.parent[my_index + c + 1]
    #         self.extend(next_item.children)
    #     # for c in range(count):
    #     #     self.parent.remove(my_index + c + 1)
        
    # def __add__(self, other):
    #     return self.parent_type(self(), other)

    # def __mul__(self, num):
    #     return self.parent_type( **[self() for i in range(num)] )

    # def index_children(self):
    #     for i, child in enumerate(self.children):
    #         child.original_index = i
    #         child.original_depthwise_index = child.depthwise_index # TO DO... this could get expensive


