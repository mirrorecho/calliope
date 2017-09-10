import calliope

class Cell(calliope.EventMachine):
    child_types = (calliope.EventMachine, )

    def __init__(self, *args, **kwargs):
        self.child_types = child_types = (calliope.Cell, calliope.Event) # just to be safe
        super().__init__(*args, **kwargs)

class TupletCell(Cell):
    proportions = (1,1,1)


class CellBlock(calliope.Block):
    # TO DO... implement this better... 
    child_types = (Cell,)
    # is_simultaneous = True
    pass



