import abjad
from calliope import tools, bubbles, machines

class CellA(machines.Cell):

    class Event1(machines.Event):
        set_beats=2
        pitch="A4"
    class Event2(machines.Event):
        set_beats=1
        pitch="B4"
    class Event3(machines.Event):
        set_beats=0.5
        pitch="C5"
    class Event4(machines.Event):
        set_beats=2
        pitch="F4"

class PhraseI(machines.Phrase):
    class CellA(CellA): pass
    class CellA1(CellA):
        class TransAccent(machines.Transform):
            def transform_nodes(self, machine):
                for node in machine:
                    node.tag(">")

        transpose_me = machines.Transpose(interval=2)


tools.illustrate_me(bubble=PhraseI)