import inspect
import abjad
from calliope import bubbles, tools, machines

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope

# class Violins(bubbles.InstrumentStaffGroup):
#     violin1 = bubbles.BubbleStaff(
#         "Violin1",
#         instrument=abjad.instrumenttools.Violin(instrument_name="Violin 1", short_instrument_name="vln.1"))
#     violin2 = bubbles.BubbleStaff(
#         "Violin2",
#         instrument=abjad.instrumenttools.Violin(instrument_name="Violin 2", short_instrument_name="vln.2"))
#     sequence = ("violin1", "violin2")

# class MyStaves(bubbles.BubbleScoreTemplate):
#     violins = Violins()
#     viola = BubbleStaff(
#         "Viola",
#         instrument=instrumenttools.Viola(instrument_name="Viola", short_instrument_name="vla"), clef="alto")
#     cello = BubbleStaff(
#         "Viola",
#         instrument=instrumenttools.Cello(instrument_name="Cello", short_instrument_name="vc"), clef="bass")
#     sequence = ("violins","viola","cello","bass")

# -------------------------------
# TO DO... CONSIDER... illustration possible here?
# tools.illustrate_me()


class MyScore(bubbles.Score):


    class Strings(bubbles.StaffGroup):
        
        class Violins(bubbles.InstrumentStaffGroup):
            class Violin1(bubbles.Staff):
                instrument=abjad.instrumenttools.Violin(
                    instrument_name="Violin 1", short_instrument_name="vln.1")
            class Violin2(bubbles.Staff):
                instrument=abjad.instrumenttools.Violin(
                    instrument_name="Violin 2", short_instrument_name="vln.2")

        class Viola(bubbles.Staff):
            instrument=abjad.instrumenttools.Viola(
                instrument_name="Viola", short_instrument_name="vla.")

        class Cello(bubbles.Staff):
            instrument=abjad.instrumenttools.Cello(
                instrument_name="Cello", short_instrument_name="vc.")
            clef="bass"

    class ShortScore1(bubbles.StaffGroup): pass

    class ShortScore2(bubbles.StaffGroup):

        class Line1(bubbles.Staff):
            color="green"

        class Line2(bubbles.Staff):
            pass

        class Line3(bubbles.Staff):
            pass

        class Line4(bubbles.Staff):
            pass



# FOR RANDOM TESTING PURPOSES ONLY:

class MyScore2(MyScore):
    pass

class MyScore3(MyScore2):
    pass

class MyScore4(MyScore3, MyScore2):
    class NewStaff(bubbles.Staff): pass
    class Strings(MyScore.Strings): pass

