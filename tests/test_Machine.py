import calliope
import abjad
import uqbar

def test_Machine_init():
    simple_cell1 = calliope.Cell("simple_cell",
        rhythm=(2,4,6,8),
        pitches=(0,2,4,6)
        )
    class SimpleCell2(calliope.Cell):
        set_name = "simple_cell"
        set_rhythm = (2,4,6,8)
        set_pitches = (0,2,4,6)

    simple_cell2 = SimpleCell2()

    assert simple_cell1.name == simple_cell2.name == "simple_cell"
    assert simple_cell1.rhythm == simple_cell2.rhythm == [2,4,6,8]
    assert simple_cell1.pitches == simple_cell2.pitches == [0,2,4,6]



def test_Machine_durations():
    # tests get_metrical_durations and get_signed_ticks_list, including rests

    c_4_4_a = calliope.Cell(rhythm=(-1,2,1.5,1.5,2,8,1.5))
    c_4_4_a_durations = c_4_4_a.get_metrical_durations()

    assert c_4_4_a_durations == [
        (1, 4), (1, 4), (1, 4), (1, 4), 
        (1, 4), (1, 4), (2, 4), 
        (4, 4), 
        (4, 4), 
        (1, 4), (1, 4),
        ]

    # ticks list, including setting rest on event
    c_4_4_a.events[1].rest = True
    ticks_list = c_4_4_a.get_signed_ticks_list()
    assert ticks_list == [-8, -16, 12, 12, 16, 64, 12]

    # test that cleanup_data combines rests
    c_4_4_a.cleanup_data()
    ticks_list = c_4_4_a.get_signed_ticks_list()
    assert ticks_list == [-24, 12, 12, 16, 64, 12]

    assert format(c_4_4_a.get_rhythm_music()) == uqbar.strings.normalize("""
    {
        r2
        r4
        c'4
        ~
        c'8
        [
        c'8
        ~
        ]
        c'4
        c'2
        c'1
        ~
        c'1
        c'4
        ~
        c'8
        [
        r8
        ]
    }""")

    # now set defined length and test get_metrical_durations get_signed_ticks_list and 
    c_4_4_a.defined_length = 20
    c_4_4_a_durations = c_4_4_a.get_metrical_durations()
    ticks_list = c_4_4_a.get_signed_ticks_list()

    assert c_4_4_a_durations == [
        (2, 4), (1, 4), (1, 4), 
        (1, 4), (1, 4), (2, 4), 
        (4, 4), 
        (4, 4), 
        (1, 4), (1, 4), (2, 4)
        ]

    assert ticks_list == [-24, 12, 12, 16, 64, 12, -20]

    assert format(c_4_4_a.get_rhythm_music()) == uqbar.strings.normalize("""
    {
        r2
        r4
        c'4
        ~
        c'8
        [
        c'8
        ~
        ]
        c'4
        c'2
        c'1
        ~
        c'1
        c'4
        ~
        c'8
        [
        r8
        ]
        r2
    }""")


def test_Machine_process_rhythm_music():
    c = calliope.Cell(
        rhythm=(1,2,3,4),
        pitches=((7,12),11,9,(12,9,6))
        )
    # make sure pitches and chords set OK in music
    assert format(c.music()) == uqbar.strings.normalize("""
        {
            <g' c''>4
            b'4
            ~
            b'4
            a'4
            ~
            a'2
            <fs' a' c''>2
            ~
            <fs' a' c''>2
        }
        """)

    c.events[0].tag(".","p", "\<")
    c.events[1].tag("(")
    c.events[-2,-1].tag(":32")
    c.events[-1].tag("ff",")")

    assert format(c.music()) == uqbar.strings.normalize("""
        {
            <g' c''>4
            \p
            -\staccato
            \<
            b'4
            ~
            (
            b'4
            a'4
            :32
            ~
            a'2
            :32
            <fs' a' c''>2
            :32
            \\ff
            ~
            <fs' a' c''>2
            :32
            )
        }
        """)


