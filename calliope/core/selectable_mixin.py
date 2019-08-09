import calliope

class SelectableMixin:
    
    # TO DO: necessary? problematic?
    @property
    def nodes(self):
        return self.depth_first()

    def depth_first(self, top_down=True):
        for item in tuple(self): # TO DO: why casting as tuple here?
            if top_down:
                yield item
            if isinstance(item, calliope.Tree):
                yield from item.depth_first(top_down=top_down)
            if not top_down:
                yield item

    def recurse(self):
        for item in self:
            yield item
            if isinstance(item, calliope.Tree):
                for sub_item in child.recurse():
                    yield sub_item

    def recurse_by_type(self, my_type):
        for item in self:
            if isinstance(item, my_type):
                yield item
            if isinstance(item, my_type._ancestor_types):
                for sub_item in item.recurse_by_type(my_type):
                    yield sub_item
    
    def select_by_type(self, my_type):
        return calliope.Selection(
            select_from=list(self.recurse_by_type(my_type)), # TO DO: is converting to a list here expensive?
            )

    # TO DO: this could handle an abstract selection
    @property
    def select(self):
        return calliope.Selection(select_from=self.children)

    def transformed(self, *args):
        """
        transforms and then returns self (in place transform)
        args should be calliope.Transform objects
        """
        for trans in args:
            trans(self)
        return self

    def print_comments(self):
        return "with %s children and %s nodes" % (len(self.children), len(list(self.depth_first()))+1)