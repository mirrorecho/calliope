import uqbar
import calliope

class LineA(calliope.Line):
    class InitialRest(calliope.RestEvent):
        set_beats=11
    class Cell1(calliope.Cell):
        set_rhythm=(1,)*4
        set_pitches=(4,6,8,None)
    class FinalRest(calliope.RestEvent):
        set_beats=13

def test_Line_replace_multimeasure_rests():
    line_a = LineA()
    # note, just testing formatting the raw music here to verify that
    # multimeasure rests OK... (as opposed to callying ly, which would
    # call process_music and add other goodies that are not part of this test)
    assert format(line_a.music()) == uqbar.strings.normalize("""
        {
            {
                R1 * 2
            }
            r2
            r4
            e'4
            fs'4
            af'4
            r2
            {
                R1 * 3
            }
        }""")