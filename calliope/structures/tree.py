import abjad

# class Tree(SetAttributeMixin, abjad.datastructuretools.TreeContainer):

class Tree(abjad.datastructuretools.TreeContainer):
    child_types = ()

    # sometimes items are moved arround... this can be used track where an element had been placed previously, which is often useful
    original_index = None 
    original_depthwise_index = None # TO DO... consider making these IndexedData objects at the parent level?

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if not self.child_types:
            self.child_types = (self.__class__,)

    def index_children(self):
        for i, child in enumerate(self.children):
            child.original_index = i
            child.original_depthwise_index = child.depthwise_index # TO DO... this could get expensive

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
        new_self = deepcopy(self)
        # for child in self.children:
        #     new_self.append(child.copy())
        return new_self

    # TO DO: still needed?
    def branch(self, *args, **kwargs):
        """
        creates a child object of type self.children_type (appending the child to self), and returns the appended child
        """
        new_branch = self.child_types[0](*args, **kwargs)
        self.append( new_branch )
        return new_branch

    def __str__(self):
        my_return_string = self.__class__.__name__ + ":" + str(self.depthwise_index)
        if self.parent and self.parent is not self.root:
            my_return_string = str(self.parent) + " | " + my_return_string
        return my_return_string
