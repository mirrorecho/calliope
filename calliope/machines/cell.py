from calliope import bubbles, machines

class Cell(machines.EventMachine):
    child_types = ()

    def __init__(self, *args, **kwargs):
        self.child_types = child_types = (machines.Cell, machines.Event)
        super().__init__(*args, **kwargs)

        # if "rhythm" in kwargs:
        #     for i, r in enumerate(kwargs["rhythm"]):
        #         if "pitches" in kwargs:
        #             pitch = kwargs["pitches"][i % len(kwargs["pitches"]) ]
        #         self["r%s" % i] = machines.Event(beats=r, pitch=pitch)


class BlockMixin(bubbles.SimulLine):

    def comp(self):
        pass

    @property
    def ticks(self):
        return max([c.ticks for c in self])


class CellBlock(BlockMixin, Cell):
    child_types = (Cell,)
    pass



