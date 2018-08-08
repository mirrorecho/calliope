import uqbar
import calliope

class PhraseA(calliope.Phrase):
    class InitialRest(calliope.RestEvent):
        set_beats=8
    class Cell1(calliope.Cell):
        set_rhythm=(0.5,0.5,0.5,0.5,)
        set_pitches=(4,6,8,9)
    class Cell2(Cell1):
        set_rhythm=(1,0.5,0.5,2)
    class Cell3(Cell1):
        set_pitches=(8,6,4,4)

def test_Selection_str():
    select = PhraseA().select
    select_string = str(select)

    assert select_string == uqbar.strings.normalize("""calliope.machines.selection.Selection() # with 4 items: [
#    test_Selection.InitialRest("InitialRest", beats=8.0, pitch=None) # with 1 children and 2 nodes
#    test_Selection.Cell1("Cell1", rhythm=[0.5, 0.5, 0.5, 0.5], pitches=[4, 6, 8, 9]) # with 4 children and 9 nodes
#    test_Selection.Cell2("Cell2", rhythm=[1.0, 0.5, 0.5, 2.0], pitches=[4, 6, 8, 9]) # with 4 children and 9 nodes
#    test_Selection.Cell3("Cell3", rhythm=[0.5, 0.5, 0.5, 0.5], pitches=[8, 6, 4, 4]) # with 4 children and 9 nodes
#    ]""")

def test_Selection_chained_str():
    p = PhraseA()
    select_1 = p.events[:-1].logical_ties(beats__gt=0.5)
    select_string_1 = str(select_1)

    assert select_string_1 == uqbar.strings.normalize("""calliope.machines.selection.Selection() # with 3 items: [
#    calliope.machines.logical_tie.LogicalTie("tie", beats=8.0, pitch=None, rest=True) # with 0 children and 1 nodes
#    calliope.machines.logical_tie.LogicalTie(beats=1.0, pitch=None, rest=False) # with 0 children and 1 nodes
#    calliope.machines.logical_tie.LogicalTie(beats=2.0, pitch=None, rest=False) # with 0 children and 1 nodes
#    ]""")

    select_2 = p.cells[0,2].select(pitch=4)
    select_string_2 = str(select_2)
    assert select_string_2 == uqbar.strings.normalize("""calliope.machines.selection.Selection() # with 3 items: [
#    calliope.machines.event.Event(beats=0.5, pitch=4) # with 1 children and 2 nodes
#    calliope.machines.event.Event(beats=0.5, pitch=4) # with 1 children and 2 nodes
#    calliope.machines.event.Event(beats=0.5, pitch=4) # with 1 children and 2 nodes
#    ]""")

