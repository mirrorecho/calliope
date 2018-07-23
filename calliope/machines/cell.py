import calliope

class Cell(calliope.EventMachine):
    child_types = (calliope.EventMachine, )

    def __init__(self, *args, **kwargs):
        self.child_types = child_types = (calliope.Cell, calliope.Event) # just to be safe
        super().__init__(*args, **kwargs)

class TupletCell(Cell):
    proportions = (1,1,1)

class CustomCell(Cell):
    child_types = ()

    def music(self, **kwargs):
        return calliope.Bubble.music(self, **kwargs)

    @property
    def ticks(self):
        return sum([l.ticks for l in self.logical_ties])

    @property
    def rest(self):
        return all([l.rest for l in self.logical_ties])

    @rest.setter
    def rest(self, is_rest):
        for l in self.logical_ties:
            l.rest = is_rest # NOTE... turning OFF rests could result in odd behavior!
            

class CellBlock(calliope.Block):
    # TO DO... implement this better... 
    child_types = (Cell,)
    # is_simultaneous = True
    pass



