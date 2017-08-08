import copy
import abjad

class BubbleMapping(object):

    def __init__(self, bubble, mapping_node, scope="children"):
        self.bubble = bubble
        self.nodes = getattr(bubble, scope)
        self.scope = scope
        self.mapping_node = mapping_node

    def filter_item(self, item):
        # TO CONSIDER... this implementation is clear and elegant,
        # but retrieval by index/slice would probably be faster (and will use simple indices/slices often)
        # ...perhaps use index/slice to retrieve whenever possible,
        # and only filter if other arguments added...?
        if self.mapping_node.query_args:
            for q in self.mapping_node.query_args:
                if type(q) is int and item is self.nodes[q]:
                    return True
                elif type(q) is slice:
                    return item in self.nodes[q]
                elif type(q) is str:
                    return item.name == q
                elif type(q) is type:
                    return type(item) == q
                # TO DO: implement lambda
                # TO DO: implement Filter object
                else:
                    pass
                    # print("WARNING: unhandled type of filter: " + str(q))
            return False
        else:
            return True
                    
    def get_filter(self):
        return filter(self.filter_item, self.nodes)

    def map_subqueries(self, as_copy=False):
        # TO DO... how to handle various types of scope at various levels?
        return_list = []
        for c in self.mapping_node.children:
            child_bubble_mapping = BubbleMapping(self.bubble, c, self.scope)
            child_filter = child_bubble_mapping.get_filter()
            for bubble_node in child_filter:
                return_list.extend( n.map_bubble( bubble_node, self.scope, as_copy) )
        return return_list

    def map_me(self, as_copy=False):
        # TO DO... add tagging
        if self.mapping_node.children:
            return self.map_subqueries 

        if as_copy:
            return [ copy.deepcopy(node) for node in self.get_filter() ]
        else:
            return list( self.get_filter() )




        # if not self.mapping_node.children:
        #     # TO DO... add tagging
        #     if as_copy:
        #         return [copy.deepcopy(node) for node in my_filter]
        #     else:
        #         return list( my_filter )

        # else:

        #     return_list = []

        #     for child_mapping_node in self.mapping_node.children:
        #         sub_bubble_mapping = BubbleMapping(self.bubble, child_mapping_node, scope)
        #         sub_bubble_filter = sub_bubble_mapping.get_filter()
        #         for bubble_node in sub_filter:
        #             return_list.extend( child_mapping_node.map_bubble( bubble_node, self.scope, as_copy) )
                
        #     return return_list


# =====================================================================================
# =====================================================================================

class MappingNode(abjad.datastructuretools.TreeContainer):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.query_args = list(args)
        self.tag_args = []
        self.tag_kwargs = {}

    # def get_filter(self, bubble, scope="children"):
    #     return BubbleMapping(bubble, self, scope).get_filter()

    def str_level(self, node, prefix=""):
        return_string = ""
        if node.query_args:
            return_string += prefix + str(node.query_args) + "\n"
        # if node.query_kwargs:
        #     return_string += prefix + str(node.query_kwargs) + "\n"
        if node.tag_args:
            return_string += prefix + str(node.tag_args) + "\n"
        if node.tag_kwargs:
            return_string += prefix + str(node.tag_kwargs) + "\n"        
        for c in node.children:
            return_string += node.str_level(c, prefix + "|    ")
        return return_string

    def __str__(self):
        # TO DO... why doesn't the TreeContainer's __str__ method apply?
        return self.str_level(self)


# =====================================================================================
# =====================================================================================

class Mapping(object):
    """
    wrapper around MappingNode with an interface to easily add
    indices, slices, filters, etc.
    """
    scope = "me" # "children"... EVENTUALLY ADD: "leaves", "nodes", ... 

    def __init__(self):
        self.map_root = MappingNode()
        self.getitem_context = self.map_root

    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (args,)
        my_node = MappingNode(*args)
        self.getitem_context.append( my_node )
        self.getitem_context = my_node
        return self

    def __call__(self, *args, **kwargs):
        self.getitem_context.tag_args.extend(args)
        self.getitem_context.tag_kwargs.update(kwargs)
        self.getitem_context = self.map_root
        return self

    def __str__(self):
        return "MAP WITH QUERY: \n" + self.map_root.__str__()

    @property
    def me(self):
        self.scope = "me"
        return self

    @property
    def children(self):
        self.scope = "children"
        return self

    @property
    def sl(self):
        return self

    def map_bubble(self, bubble, scope="children", as_copy=False):

        bubble_mapping = BubbleMapping(bubble, self.map_root, scope)
        return bubble_mapping.map_me(as_copy)

# =====================================================================================
# =====================================================================================

class Filter(object):
    pass



