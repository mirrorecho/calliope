import calliope


class Block(calliope.BaseMachine, calliope.SimulFragment):

    def comp(self): #TO DO ????????
        pass

    @property
    def ticks(self):
        return max([c.ticks for c in self])

# TO DO: consider... can blocks contain blocks?

class EventBlock(Block):
    # TO DO... implement this better... 
    child_types = (calliope.Event,)

# class CellBlock(Block, calliope.Machine): #... TO DO: what would have been the purpose of this?
class CellBlock(Block):
    # TO DO... implement this better... 
    child_types = (calliope.Cell,)

class PhraseBlock(Block):
    child_types = (calliope.Phrase,)

class LineBlock(Block):
    # TO DO... implement this better... 
    child_types = (calliope.Line,)
    # is_simultaneous = True

# TO DO: consider... add LogicalTieBlock? (really just a chord?)