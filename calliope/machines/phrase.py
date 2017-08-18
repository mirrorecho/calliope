import calliope

class Phrase(calliope.EventMachine):
    child_types = (calliope.Cell, calliope.Event)

class PhraseBlock(calliope.Block, Phrase):
    child_types = (Phrase,)
    pass