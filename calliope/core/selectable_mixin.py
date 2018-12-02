import calliope

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
        # print(args)
        return calliope.Selection(
            select_from=self.get_nodes(), 
            type_args=args
            )

    @property
    def select(self):
        return calliope.Selection(select_from=self.children)

    # @classmethod
    # def set_select_property(cls, name, select_type):
    #     setattr(cls, name, property(lambda x: x.select_by_type(select_type)))

    # @classmethod
    # def set_select_property_callable(cls, name, select_type):
    #     setattr(cls, name, property(callable))

    def print_comments(self):
        return "with %s children and %s nodes" % (len(self.children), len(list(self.depth_first()))+1)