import calliope


class FragmentBlock(calliope.Fragment):
    is_simultaneous = True
    sort_init_attrs = ("transpose",)

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

    def to_block_list(self):
        my_length = len(self)
        return [
            node.block_type(
                *[self[i][j]() for i in range(my_length)],
                name = (self[0][j].name if self[0][j].name else self[0][j].__class__.__name__.lower()) +  "_block" + str(j),
            ) for j, node in enumerate(self[0])
            ]

    @classmethod
    def from_block_list(cls, block_list):
        my_length = len(block_list[0])
        child_type = cls.child_types[0]
        child_rows = []

        for i in range(my_length):
            child_row = child_type()
            for block in block_list:
                child_row.append(block[i]())
            child_rows.append(child_row)

        return cls(*child_rows)

    def to_score(self, *args, **kwargs):
        return calliope.Score(
            *[calliope.Staff(n()) for n in self],
            *args,
            **kwargs
            )

        # TO DO... this would be more elegant, but has an issue...
        # return cls(
        #     *[cls.child_types[0](
        #         *[node() for block in block_list for node in block[i] ]
        #         ) for i in range(my_length)]
        #     )


# TO DO: consider... can blocks contain blocks?

class EventBlock(FragmentBlock):
    # TO DO... implement this better... 
    child_types = (calliope.Event,)

# class CellBlock(Block, calliope.Machine): #... TO DO: what would have been the purpose of this?
class CellBlock(FragmentBlock):
    # TO DO... implement this better... 
    child_types = (calliope.Cell,)

class PhraseBlock(FragmentBlock):
    child_types = (calliope.Phrase, calliope.Cell,)

class LineBlock(FragmentBlock):
    child_types = (calliope.Line, calliope.Phrase, calliope.Cell,)

class SegmentBlock(FragmentBlock):
    # TO DO... implement this better... 
    # TO DO... consider a Section class here with more section-specific stuff
    child_types = (calliope.Segment, calliope.Line, calliope.Phrase, calliope.Cell,)
    # is_simultaneous = True

# maybe this should go on Score.startup_root ...?
setattr(calliope.Segment, "block_type", SegmentBlock)
setattr(calliope.Line, "block_type", LineBlock)
setattr(calliope.Phrase, "block_type", PhraseBlock)
setattr(calliope.Cell, "block_type", CellBlock)
setattr(calliope.Event, "block_type", EventBlock)

SegmentBlock.startup_root()
LineBlock.startup_root()
PhraseBlock.startup_root()
CellBlock.startup_root()
EventBlock.startup_root()


