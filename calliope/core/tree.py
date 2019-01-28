import inspect
import copy
import re
# import itertools # may consider using

import calliope

from .tree_node import TreeNode

TREE_CONTAINER_MRO_COUNT = len(inspect.getmro(TreeNode))

# SEE COMMENT AT: https://gist.github.com/jaytaylor/3660565
def camel_to_snake(s):
    return re.sub("([A-Z])", "_\\1", s).lower().lstrip("_")


### ---------------------------------------------------------------------------- ###
### ---------------------------------------------------------------------------- ###
# INSPIRED BY: https://github.com/josiah-wolf-oberholtzer/uqbar/blob/master/uqbar/containers/UniqueTreeContainer.py
### ---------------------------------------------------------------------------- ###

class Tree(calliope.SelectableMixin, TreeNode):
    child_types = () # TO DO, consider indicating private
    select_property = None # TO DO, consider indicating private
    set_name = None

    _descendant_types = ()

    def __init__(self, *args, **kwargs):
        super().__init__(args) # args sets children here...
        self._children = []
        self._named_children = {}

        if len(args) > 0 and isinstance(args[0], str):
            my_name = args[0]
            args = args[1:]
        else:
            my_name = self.set_name
       
        TreeNode.__init__(self, name=my_name)

        if args:
            self[:] = args

        self.setup(**kwargs)
        self.set_children_from_class(**kwargs)

        # if not self.child_types:
        #     self.child_types = (Tree,)

    # can be overriden to set children based on other/special logic
    # TO DO: consider merging with CopyChildrenBubble.set_children used in a couple places
    def set_children_from_class(self, **kwargs):
        for node_name in type(self).class_sequence(): 
            node = getattr(self, node_name)
            self[camel_to_snake(node_name)] = node


    @classmethod
    def _set_relation_types(cls, ancestor_types=()):
        """
        Called to set _parent_types, _ancestor_types, and _descendant_types
        """
        if cls not in ancestor_types:
            ancestor_types += (cls,)
        
        for child_type in cls.child_types:
            if cls not in child_type._parent_types:
                child_type._parent_types += (cls,)
                child_type._ancestor_types += tuple(
                    [t for t in ancestor_types if t not in child_type._ancestor_types]
                    )
                for ancestor_type in ancestor_types:
                    if child_type not in ancestor_type._descendant_types:
                        ancestor_type._descendant_types += (child_type,)
                child_type._set_relation_types(ancestor_types)


    @classmethod
    def startup_root(cls):        
        """
        Called on tree root class to set various attributes
        """
        cls._set_relation_types()

        for c in (cls,) + cls._descendant_types:
            # TO DO: consider setting _descendant_types and _ancestor_types here
            for child_type in c.child_types:
                # TO DO: set_tree_select_property DOES NOT WORK HERE... 
                # only set_tree_by_type_property ... something with the lamda ??????
                c.set_tree_by_type_property(
                    child_type.select_property,
                    child_type,
                    )

    @classmethod
    def set_tree_select_property(cls, name, callable):
        """
        creates new properties on Tree classes that return selections. Adds the same properties to 
        the Tree's "ancestor" classes so that all matching descendants can be selected
        """
        # selections have all select properties
        setattr(calliope.Selection, name, property(callable))

        for set_on_cls in (cls,) + cls._ancestor_types:
            # print(set_on_cls, name, c)
            setattr(set_on_cls, name, property(callable))
            # setattr(set_on_cls, name + "_YO", c.__name__)
            # setattr(set_on_cls, name + "_YA", property(lambda x: x.select_by_type(c)))


    @classmethod
    def set_tree_by_type_property(cls, name, select_type):
        cls.set_tree_select_property(
            name,
            lambda x: x.select_by_type(select_type),
            )


    def __call__(self, name=None, **kwargs):
        return_node = copy.deepcopy(self)
        if name:
            return_node.name = name # TO DO: ????
        for name, value in kwargs.items():
            setattr(return_node, name, value)
        return return_node

    def __setitem__(self, key, expr):
        if inspect.isclass(expr):
            expr = expr()
        # print(expr)
        if isinstance(key, (int,str)):

            if not isinstance(expr, self.child_types):
                # print(self.child_types)
                # print(node)
                self.warn("attempted to add child but not an allowed child type - child not added", expr)

            else:

                # THIS WAS IN UQBAR BUT HOOK WITH NOTHING (NOT USED):
                # expr = self._prepare_setitem_multiple(expr)
                               
                if expr in self.parentage:
                    raise ValueError('Cannot set parent node as child.')

                new_child = True

                if isinstance(key, str):
                    my_index = next((i for i, c in enumerate(self.children) if c.name==key), None)
                    if my_index is None:
                        expr.name = key
                        self.append(expr)
                else:
                    my_index = key

                if my_index is not None:
                    old = self[my_index]
                    old._set_parent(None)

                    expr._set_parent(self)
                    self._children.insert(key, expr)


        elif isinstance(key, slice):
            
            # THIS WAS IN UQBAR BUT HOOK WITH NOTHING (NOT USED):
            # expr = self._prepare_setitem_multiple(expr)
            
            if isinstance(expr, calliope.Tree):
                # Prevent mutating while iterating by copying.
                expr = expr[:]
            
            # TO DO: consider more forgiving warning here instead of assert?
            assert all(isinstance(x, self.child_types) for x in expr) 
            
            if key.start == key.stop and key.start is not None \
                and key.stop is not None and key.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = key.indices(len(self))
            
            old = self[start:stop]
            parentage = self.parentage
            
            if any(node in parentage for node in expr):
                raise ValueError('Cannot set parent node as child.')
            
            for node in old:
                node._set_parent(None)
            
            for node in expr:
                node._set_parent(self)

            # node.name = arg # just as a precaution
            # new_child = True
            # for i, b in enumerate(self.children):
            #     if b.name == arg:
            #         UniqueTreeContainer.__setitem__(self, i, node)
            #         new_child = False
            #         break
            # if new_child:
            #     UniqueTreeContainer.__setitem__(self,
            #         slice(len(self), len(self)),
            #         [node]
            #         )


            self._children.__setitem__(slice(start, start), expr)

        self._mark_entire_tree_for_later_update()


    # TO DO: is this duplicative?
    @property
    def child_names(self):
        return [c.name for c in self]

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

    # TO DO... CONSIDER THIS FOR 'ABSTRACT' SELECTIONS
    # not currently working...
    def select_with(self, selection):
        selection.innermost_selection.select_from = self
        return selection

    ### ---------------------------------------- ###
    ### ---------------------------------------- ###
    ### moved from uqbar.UniqueTreeContainer:
    ### ---------------------------------------- ###

    def __contains__(self, expr):
        if isinstance(expr, str):
            return expr in self._named_children
        for x in self._children:
            if x is expr:
                return True
        return False

    def __delitem__(self, i):
        if isinstance(i, str):
            children = tuple(self._named_children[i])
            for child in children:
                parent = child.parent
                del(parent[parent.index(child)])
            return
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        self.__setitem__(i, [])
        self._mark_entire_tree_for_later_update()

    def __getitem__(self, expr):
        if isinstance(expr, (int, slice)):
            return self._children[expr]
        elif isinstance(expr, str):
            result = sorted(
                self._named_children[expr],
                key=lambda x: x.graph_order,
                )
            if len(result) == 1:
                return result[0]
            return result
        raise ValueError(expr)

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
        return len(self._children)

    def _cache_named_children(self):
        name_dictionary = super(Tree, self)._cache_named_children()
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        return name_dictionary

    ### PRIVATE PROPERTIES ###

    ### PUBLIC METHODS ###

    def append(self, expr):
        ## TO DO: ????
        self.__setitem__(
            slice(len(self), len(self)),
            [expr]
            )

    def extend(self, expr):
        self.__setitem__(
            slice(len(self), len(self)),
            expr
            )

    def index(self, expr):
        for i, child in enumerate(self._children):
            if child is expr:
                return i
        else:
            message = '{!r} not in {!r}.'
            message = message.format(expr, self)
            raise ValueError(message)

    def insert(self, i, expr):
        self.__setitem__(
            slice(i, i),
            [expr]
            )

    def pop(self, i=-1):
        node = self[i]
        del(self[i])
        return node

    def remove(self, node):
        i = self.index(node)
        del(self[i])

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)


    ### ---------------------------------------- ###
    ### ---------------------------------------- ###
    ### new implementations based on move from uqbar
    ### ---------------------------------------- ###    
    

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


