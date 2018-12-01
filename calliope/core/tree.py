import inspect
import copy
import abjad
import uqbar
import calliope

TREE_CONTAINER_MRO_COUNT = len(inspect.getmro(uqbar.containers.UniqueTreeContainer))

class Tree(calliope.SelectableMixin, uqbar.containers.UniqueTreeContainer):
    child_types = () # TO DO, consider indicating private
    select_property = None # TO DO, consider indicating private
    set_name = None

    _parent_types = ()

    
    # # KISS!
    # parent_type = None 
    # original_index = None 
    # original_depthwise_index = None # TO DO... consider making these IndexedData objects at the parent level?


    # can be overriden to set children based on other/special logic
    # TO DO: consider merging with CopyChildrenBubble.set_children used in a couple places
    def set_children_from_class(self, **kwargs):
        for node_name in type(self).class_sequence(): 
            node = getattr(self, node_name)
            self[node_name] = node

    # TO DO: consider setting as new attribute (for performance)
    @classmethod
    def get_ancestor_types(cls, ancestors=() ):
        for parent in cls._parent_types:
            if parent not in ancestors:
                ancestors += (parent,)
                parent_ancestors = parent.get_ancestor_types(ancestors)
                ancestors += tuple([p for p in parent_ancestors if p not in ancestors])
        return ancestors

    # TO DO: consider setting as new attribute (for performance)
    @classmethod
    def get_descendant_types(cls, descendants=() ):
        for child in cls.child_types:
            if child not in descendants:
                descendants += (child,)
                child_descendants = child.get_descendant_types(descendants)
                descendants += tuple([c for c in child_descendants if c not in descendants])
        return descendants

    @classmethod
    def _set_parent_types(cls):
        """
        Called on tree root class to set parent_types
        """
        for child in cls.child_types:
            if cls not in child._parent_types:
                child._parent_types += (cls,)
                child._set_parent_types()


    @classmethod
    def startup(cls):        
        """
        Called on tree root class to set various attributes
        """
        cls._set_parent_types()

        for c in (cls,) + cls.get_descendant_types():
            # TO DO: consider setting _descendant_types and _ancestor_types here
            for child_type in c.child_types:
                c.set_tree_select_property(
                    child_type.select_property,
                    lambda x: x.select_by_type(child_type)
                    )

    @classmethod
    def set_tree_select_property(cls, name, callable):
        """
        creates new properties on Tree classes that return selections. Adds the same properties to 
        the Tree's "ancestor" classes so that all matching descendants can be selected
        """
        # selections have all select properties
        setattr(calliope.Selection, name, property(callable))

        for set_on_cls in (cls,) + cls.get_ancestor_types():

            setattr(set_on_cls, name, property(callable))            


    def __init__(self, *args, **kwargs):
        super().__init__(args) # args sets children here...
        if self.set_name:
            self.name = self.set_name
        self.setup(**kwargs)
        self.set_children_from_class(**kwargs)
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


