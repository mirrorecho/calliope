import calliope

class SelectableMixin(calliope.BaseMixin):
    

    def recurse_by_type(self, my_type):
        for sub_item in self:
            if isinstance(sub_item, my_type):
                yield sub_item
            if isinstance(sub_item, my_type.get_ancestor_types()):
                for grandchild in sub_item.recurse_by_type(my_type):
                    yield grandchild

    def select_by_type(self, my_type):
        # print(args)
        return calliope.Selection(
            select_from=self.recurse_by_type(my_type), 
            # type_args=args
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