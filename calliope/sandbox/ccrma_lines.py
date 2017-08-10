import abjad
from calliope import tools, bubbles, machines


class ScoreDemo(bubbles.Score):

    class Flute(bubbles.Staff):
        instrument=abjad.instrumenttools.Flute(
            instrument_name="Flute", short_instrument_name="fl.")

    class Clarinet(bubbles.Staff):
        instrument=abjad.instrumenttools.ClarinetInBFlat(
            instrument_name="Clarinet in Bb", short_instrument_name="cl.")

    class MyStaffGroup(bubbles.StaffGroup):
        class Violin1(bubbles.Staff):
            instrument=abjad.instrumenttools.Violin(
                instrument_name="Violin 1", short_instrument_name="vln.")

        class Violin2(bubbles.Staff):
            instrument=abjad.instrumenttools.Violin(
                instrument_name="Violin 2", short_instrument_name="vln.")



# ==============================================

tools.illustrate_me(  )