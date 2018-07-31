import calliope
import abjad
import uqbar

def test_Bubble_music():
    music_contents = "c4 c4 c4 c4"

    abjad_container = abjad.Container(music_contents)
    my_bubble = calliope.Bubble(music_contents=music_contents, is_simultaneous=False)
    music = my_bubble.music()

    assert isinstance(music, abjad.Container)
    assert format(my_bubble.music()) == uqbar.strings.normalize("""
        { 
            c4 
            c4 
            c4 
            c4
        }
        """)
