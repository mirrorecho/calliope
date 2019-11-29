import abjad
import calliope


# TO DO: use abjad lable to make this more elegant ... 
class Label(calliope.Transform):
    attrs=("selection_index",)

    # TO DO: move this to a class attribute for any calliope.Tree class
    def label_prefix(self, node):
        if isinstance(node, calliope.Segment):
            return "seg."
        if isinstance(node, calliope.Line):
            return "l."
        if isinstance(node, calliope.Phrase):
            return "p."
        if isinstance(node, calliope.Cell):
            return "c."
        else:
            return ""

    def transform(self, selectable, **kwargs):
        for i, n in enumerate(selectable):
            for attr in self.attrs:
                value = i if attr == "selection_index" else getattr(n,attr,None)
                # print(n, attr, value)
                if value is not None:
                    n.tag(self.label_prefix(n)+str(value))


    # TO DO: useful, or KISS?
    # @classmethod
    # def make(cls, callable, **kwargs):
    #     my_transform = cls(**kwargs)
    #     my_transform.transform = callable
    #     return my_transform



