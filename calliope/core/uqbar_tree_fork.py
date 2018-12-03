# ORIGINAL: https://github.com/josiah-wolf-oberholtzer/uqbar/blob/master/uqbar/containers/UniqueTreeNode.py

import collections
import copy
import typing


class UniqueTreeNode:
    """
    A node in a "unique" tree.
    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### CLASS VARIABLES ###

    _state_flag_names: typing.Tuple[str, ...] = ()

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

### ---------------------------------------------------------------------------- ###
### ---------------------------------------------------------------------------- ###
# ORIGINAL: https://github.com/josiah-wolf-oberholtzer/uqbar/blob/master/uqbar/containers/UniqueTreeNode.py
### ---------------------------------------------------------------------------- ###

class UniqueTreeContainer(UniqueTreeNode):
    """
    A container node in a "unique" tree.
    Container nodes may contain zero or more other nodes.
    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._children = []
        self._named_children = {}
        if children is not None:
            self[:] = children

    ### SPECIAL METHODS ###

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

    # INTEGRATED INTO calliope.Tree
    # def __setitem__(self, i, expr):
    #     if isinstance(i, int):
    #         expr = self._prepare_setitem_single(expr)
    #         assert isinstance(expr, self._node_class)
    #         old = self[i]
    #         if expr in self.parentage:
    #             raise ValueError('Cannot set parent node as child.')
    #         old._set_parent(None)
    #         expr._set_parent(self)
    #         self._children.insert(i, expr)
    #     else:
    #         expr = self._prepare_setitem_multiple(expr)
    #         if isinstance(expr, UniqueTreeContainer):
    #             # Prevent mutating while iterating by copying.
    #             expr = expr[:]
    #         assert all(isinstance(x, self._node_class) for x in expr)
    #         if i.start == i.stop and i.start is not None \
    #             and i.stop is not None and i.start <= -len(self):
    #             start, stop = 0, 0
    #         else:
    #             start, stop, stride = i.indices(len(self))
    #         old = self[start:stop]
    #         parentage = self.parentage
    #         if any(node in parentage for node in expr):
    #             raise ValueError('Cannot set parent node as child.')
    #         for node in old:
    #             node._set_parent(None)
    #         for node in expr:
    #             node._set_parent(self)
    #         self._children.__setitem__(slice(start, start), expr)
    #     self._mark_entire_tree_for_later_update()

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = super(UniqueTreeContainer, self)._cache_named_children()
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        return name_dictionary

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return UniqueTreeNode

    ### PUBLIC METHODS ###

    def append(self, expr):
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