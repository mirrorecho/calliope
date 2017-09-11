import abjad, calliope
from calliope.sandbox import module_0, module_a

class SimpleScore(calliope.Score):

    class Flute(calliope.Staff):
        instrument=abjad.instrumenttools.Flute(
            instrument_name="Flute", short_instrument_name="fl.")

    class Clarinet(calliope.Staff):
        instrument=abjad.instrumenttools.ClarinetInBFlat(
            instrument_name="Clarinet in Bb", short_instrument_name="cl.")

    class StringsStaffGroup(calliope.StaffGroup):
        class Violin(calliope.Staff):
            instrument=abjad.instrumenttools.Violin(
                instrument_name="Violin", short_instrument_name="vln.")

        class Cello(calliope.Staff):
            instrument=abjad.instrumenttools.Violin(
                instrument_name="Cello", short_instrument_name="vc.")
            yo = calliope.Fragment(
                music_contents = "c1 d1",
                clef = "bass"
                )

short_score = calliope.MatchSequence(
    calliope.Bubble.from_module(module_0, name="section_0"),
    calliope.Bubble.from_module(module_a, name="section_a"),
)

# TO DO: something like this should work:
# short_score["section_0"].append(calliope.Fragment("e''2", name="Clarinet"))

# short_score_inverted = short_score.get_inverted()
# print(short_score_inverted.ly())

# calliope.illustrate_me(score_type=SimpleScore, bubble=short_score())







