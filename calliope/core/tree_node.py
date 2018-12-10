import collections
import copy
import typing

### ---------------------------------------------------------------------------- ###
### ---------------------------------------------------------------------------- ###
# INSPIRED BY: https://github.com/josiah-wolf-oberholtzer/uqbar/blob/master/uqbar/containers/UniqueTreeNode.py
### ---------------------------------------------------------------------------- ###


class TreeNode:
    """
    A node in a "unique" tree.
    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### CLASS VARIABLES ###
    # ???????????
    _state_flag_names: typing.Tuple[str, ...] = ()

    _parent_types = ()
    _ancestor_types = ()


    ### INITIALIZER ###

    def __init__(self, name: str=None) -> None:
        self._name = name
        self._parent = None

    ### PRIVATE METHODS ###


    def _cache_named_children(self):
        name_dictionary = {}
        if self.name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = set()
            name_dictionary[self.name].add(self)
        return name_dictionary

    ### ---------------------------------------- ###
    ### UNUSED METHODS FROM uqbar.UniqueTreeNode ###
    ### TO DO: what was the purpose of these?    ###
    ### ---------------------------------------- ###

    # @classmethod
    # def _iterate_nodes(cls, nodes):
    #     for x in nodes:
    #         yield x
    #         if hasattr(x, '_children'):
    #             for y in cls._iterate_nodes(x):
    #                 yield y

    # def _get_node_state_flags(self):
    #     state_flags = {}
    #     for name in self._state_flag_names:
    #         state_flags[name] = True
    #         for node in self.parentage:
    #             if not getattr(node, name):
    #                 state_flags[name] = False
    #                 break
    #     return state_flags

    ### ---------------------------------------- ###


    def _mark_entire_tree_for_later_update(self):
        for node in self.parentage:
            for name in self._state_flag_names:
                setattr(node, name, False)

    def _remove_from_parent(self):
        if self._parent is not None:
            if self in self._parent:
                self._parent._children.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.parentage[1:]:
                named_children = parent._named_children
                for name in name_dictionary:
                    for node in name_dictionary[name]:
                        named_children[name].remove(node)
                    if not named_children[name]:
                        del(named_children[name])

    def _restore_named_children_to_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.parentage[1:]:
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].update(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

    def _set_parent(self, new_parent):
        named_children = self._cache_named_children()
        self._remove_named_children_from_parentage(named_children)
        self._remove_from_parent()
        self._parent = new_parent
        self._restore_named_children_to_parentage(named_children)
        self._mark_entire_tree_for_later_update()

    ### ---------------------------------------- ###
    ### PUBLIC METHODS from uqbar.UniqueTreeNode ###
    ### TO DO: keep?
    ### ---------------------------------------- ###


    def precede_by(self, expr):
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index:index] = expr

    def replace_with(self, expr):
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index:index + 1] = expr

    def succeed_by(self, expr):
        if not isinstance(expr, collections.Sequence):
            expr = [expr]
        index = self.parent.index(self)
        self.parent[index + 1:index + 1] = expr

    ### ---------------------------------------- ###

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        return len(self.parentage) - 1

    @property
    def graph_order(self):
        parentage = tuple(reversed(self.parentage))
        graph_order = []
        for i in range(len(parentage) - 1):
            parent, child = parentage[i:i + 2]
            graph_order.append(parent.index(child))
        return tuple(graph_order)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, expr):
        assert isinstance(expr, (str, type(None)))
        old_name = self._name
        for parent in self.parentage[1:]:
            named_children = parent._named_children
            if old_name is not None:
                named_children[old_name].remove(self)
                if not named_children[old_name]:
                    del named_children[old_name]
            if expr is not None:
                if expr not in named_children:
                    named_children[expr] = set([self])
                else:
                    named_children[expr].add(self)
        self._name = expr

    @property
    def parent(self):
        return self._parent

    @property
    def parentage(self):
        parentage = []
        node = self
        while node is not None:
            parentage.append(node)
            node = node.parent
        return tuple(parentage)

    @property
    def root(self):
        proper_parentage = self.parentage[1:]
        if not proper_parentage:
            return None
        return proper_parentage[-1]