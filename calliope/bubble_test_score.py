import abjad
from callope import bubbles

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope

class Violins(bubbles.InstrumentStaffGroup):
    violin1 = bubbles.BubbleStaff(
        "Violin1",
        instrument=abjad.instrumenttools.Violin(instrument_name="Violin 1", short_instrument_name="vln.1"))
    violin2 = bubbles.BubbleStaff(
        "Violin2",
        instrument=abjad.instrumenttools.Violin(instrument_name="Violin 2", short_instrument_name="vln.2"))

class MyScore(bubbles.BubbleScore):
    violins = CopperViolinIDiv()
    viola = BubbleStaff(
        "Viola",
        instrument=instrumenttools.Viola(instrument_name="Viola", short_instrument_name="vla"), clef="alto")
    cello = BubbleStaff(
        "Viola",
        instrument=instrumenttools.Cello(instrument_name="Cello", short_instrument_name="vc"), clef="bass")
    sequence = ("violins","viola","cello","bass")

# -------------------------------

bubbles.illustrate_me()