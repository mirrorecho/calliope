import calliope
import abjad
import uqbar

class PhraseA(calliope.Phrase):
    class InitialRest(calliope.RestEvent):
        set_beats=4
    class Cell1(calliope.Cell):
        set_rhythm=(1,1,1,1)
        set_pitches=(0,2,3,5)
    class Cell2(Cell1):
        set_rhythm=(1,0.5,0.5,2)
    class Cell3(Cell1):
        set_pitches=(7,5,3,2)

def test_MachineSelectableMixin_cells():
    
    p = PhraseA()
    cells_select = p.cells

    assert isinstance(cells_select, calliope.Selection)
    assert len(cells_select) == 3
    for c in cells_select:
        assert isinstance(c, calliope.Cell)
    assert list(p.cells) == [p[1], p[2], p[3]]

def test_MachineSelectableMixin_events_kwargs():
    
    p = PhraseA()
    events_select = p.events(pitch__lt=1, pitch__gt=3)

    assert isinstance(events_select, calliope.Selection)
    assert len(events_select) == 6
    for e in events_select:
        assert isinstance(e, calliope.Event)
        assert e.pitch < 1 or e.pitch > 3

    non_rest_events = p.non_rest_events
    assert len(non_rest_events) == 12
    for e in non_rest_events:
        assert not isinstance(e, calliope.RestEvent)
        assert not e.rest





