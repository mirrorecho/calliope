import uqbar
import calliope

class FragmentA(calliope.Fragment):
    music_contents = "e'2. R2."
    time_signature = (3,4)
    clef = "bass"

class FragmentB(calliope.Fragment):
    music_contents = "cs'2. d'2 r4 b2."
    bar_line = "!"

def test_Fragment():
    my_fragment = calliope.Fragment(FragmentA(), FragmentB())
    assert my_fragment.ly() == uqbar.strings.normalize(r"""
        {
            {
                \numericTimeSignature
                \time 3/4
                \clef "bass"
                e'2.
                R2.
            }
            {
                \bar "!"
                cs'2.
                d'2
                r4
                b2.
            }
        }""")