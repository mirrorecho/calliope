import calliope


class FragmentBlock(calliope.Fragment):
    is_simultaneous = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_attributes_on_child_lines(
            "meter", 
            "defined_length", 
            "bookend_rests",
            "time_signature",
            "pickup",
            "bar_line"
            )


    def set_attributes_on_child_lines(self, *args):
        for name in args:
            value = getattr(self, name, None)
            if value:
                for child_line in self:
                    setattr(child_line, name, value)

    def add_bookend_rests(self, beats_before=0, beats_after=0):
        for child_line in self:
            child_line.add_bookend_rests(beats_before, beats_after)

    # TO DO: consider making this cyclic???
    def remove_bookend_rests(self):
        for child_line in self:
            child_line.remove_bookend_rests()

    @property
    def ticks(self):
        return max([c.ticks for c in self])


# TO DO: consider... can blocks contain blocks?

class EventBlock(FragmentBlock):
    # TO DO... implement this better... 
    child_types = (calliope.Event,)

# class CellBlock(Block, calliope.Machine): #... TO DO: what would have been the purpose of this?
class CellBlock(FragmentBlock):
    # TO DO... implement this better... 
    child_types = (calliope.Cell,)

class PhraseBlock(FragmentBlock):
    child_types = (calliope.Phrase,)

class LineBlock(FragmentBlock):
    child_types = (calliope.Line,)

class SegmentBlock(FragmentBlock):
    # TO DO... implement this better... 
    # TO DO... consider a Section class here with more section-specific stuff
    child_types = (calliope.Segment,)
    # is_simultaneous = True

# TO DO: consider... add LogicalTieBlock? (really just a chord?)