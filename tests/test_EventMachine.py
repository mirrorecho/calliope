import calliope
import uqbar

class PhraseA(calliope.Phrase):
    class InitialRest(calliope.RestEvent):
        set_beats=4
    class Cell1(calliope.Cell):
        set_rhythm=(-1,1,-1,1)
    class Cell2(calliope.Cell):
        set_rhythm=(1,0.5,0.5,2)
    class Cell3(Cell1):
        set_pitches=(2,2,2,None)

def test_EventMachine_set_pitches():
    p_class_a = PhraseA()
    p_args_a = calliope.Phrase(
        calliope.RestEvent(beats=4),
        calliope.Cell(rhythm=(-1,1,-1,1)),
        calliope.Cell(rhythm=(1,0.5,0.5,2)),
        calliope.Cell(rhythm=(-1,1,-1,1), pitches=(2,2,2,None)),
        )
    # verify that correct pitches/rests set when instantiated from class or from kwargs
    assert p_class_a.ly() == p_args_a.ly() == uqbar.strings.normalize(r"""
        {
            r1
            r4
            c'4
            r4
            c'4
            c'4
            c'8
            [
            c'8
            ]
            c'2
            d'4
            d'4
            d'4
            r4
        }""")

    # verify that pithes/rests can be reset OK   
    p_class_a = PhraseA()
    p_class_a.pitches= [0,1,2,3,4,5,6,7,8,9,None,None,12]
    p_class_a.events[3].rest = True

    assert p_class_a.ly() == uqbar.strings.normalize(r"""
        {
            c'1
            cs'4
            d'4
            r4
            e'4
            f'4
            fs'8
            [
            g'8
            ]
            af'2
            a'4
            r4
            r4
            c''4
        }""")

    class PhraseANew(PhraseA):
        set_pitches=(0,None,4)*4 + (2,)
    
    p_class_a_new = PhraseANew()
    p_class_a = PhraseA()
    p_class_a.pitches=(0,None,4)*4 + (2,)
    
    assert p_class_a_new.pitches == p_class_a.pitches

    assert p_class_a_new.ly() == p_class_a.ly() == uqbar.strings.normalize(r"""
        {
            c'1
            r4
            e'4
            c'4
            r4
            e'4
            c'8
            [
            r8
            ]
            e'2
            c'4
            r4
            e'4
            d'4
        }
        """)

    # verify that pithes reset OK when if skipping rests on new instance of class


