from calliope import bubbles, machines

class Cell(machines.EventMachine):
    child_types = (machines.EventMachine, )

    def __init__(self, *args, **kwargs):
        self.child_types = child_types = (machines.Cell, machines.Event) # just to be safe
        super().__init__(*args, **kwargs)

class CellBlock(machines.BlockMixin, Cell):
    child_types = (Cell,)
    pass



