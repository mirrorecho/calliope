from calliope import machines

class Phrase(machines.EventMachine):
    child_types = (machines.Cell, machines.Event)

class PhraseBlock(machines.Block, Phrase):
    child_types = (Phrase,)
    pass