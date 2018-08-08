import calliope
import abjad
import uqbar

def test_Bubble_music():
    music_contents = "c4 c4 c4 c4"

    abjad_container = abjad.Container(music_contents)
    my_bubble = calliope.Bubble(music_contents=music_contents, is_simultaneous=False)
    music = my_bubble.music()

    assert isinstance(music, abjad.Container)
    # these should all be equivalent  since ly calls blow and formats, and blow calls music/process_music
    # (but process_music on the Bubble base class is a hook that does nothing)
    assert format(music) == format(my_bubble.blow()) == my_bubble.ly() == uqbar.strings.normalize("""
        { 
            c4 
            c4 
            c4 
            c4
        }
        """)
