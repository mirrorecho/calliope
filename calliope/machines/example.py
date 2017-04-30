from calliope import structures, machines

class CopperPhrase(InventoryBasedPhrase):
    pitch_cell_inventory = structures.SeriesCollection({
        "hi": ( 2, 0,-1),
        "low": (-5,-3,-1),
        "mid": (-3, 0,-1),
        })
    rhythm_cell_inventory = structures.SeriesCollection({
        "medium": (2, 1, 1),
        "short": (1, 1, 1),
        "long": (4, 1, 1),
    })


class Phrase1(CopperPhrase):
    cell1 = Cell(pitches="hi", rhythm="medium")
    cell2 = Cell(pitches="hi", rhythm="medium")

class Phrase2(CopperPhrase1):
    cell2 = Cell(pitches="mid", rhythm="medium")
    cell3 = Cell(pitches="mid", rhythm="short")

class Phrase3(CopperPhrase1):
    cell1 = Cell(pitches="hi", rhythm="long")

class Phrase4(CopperPhrase1):
    cell3 = Cell(pitches="mid", rhythm="short")



class LineMixin(object): # basic attributes, such as starting time signature, rehearsal mark, etc.
    metrical_durations = structures.Series(default=((4,4),), limit=12)
    # tempo_units_per_minute = 48 # TO DO... tempo indication makes everything SLOW... WHY?????
    # tempo_text = "Slow"
    tempo_command = '\\note #"4" #1 = 48'
    # tempo_units_per_minute = 48
    time_signature = (4,4)


class BaseLine(LineMixin, machines.PitchedMachine):
    phrase1 = CopperPhrase1()
    phrase2 = CopperPhrase2()
    phrase3 = CopperPhrase3()
    phrase4 = CopperPhrase4()

    rhythm_initial_silence = 1
    rhythm_times = 1



class LineRhythmsDeveloped1(machines.RhythmsMultiplied, CopperLine):
    slow_p1 = DefRhythmsMultiplied(all=2, phrase1=1, cell1=0.5)
    break_phrases =  DefRhythmsExtendLongNotes(phrase1=1, cell1=2)
    pulse_ending = DefRhythmsPulsed(phrase4=1, cell2=0.25)


# TO DO .... add ArrangedLine to bubbles
class MusicBase(LineMixin, bubbles.ArrangedLine):
    unarranged = None # this is what to output if line is not arranged
    line0 = BaseLine()
    line1 = LineRhythmsDeveloped1()
    # show_data_attr="depthwise_index"
    respell="sharps"

class Flute1(MusicBase):

    bite1 = Bites(
        Off("line0", phrase)[3:4](),


        Off(line=2)[7:10](
                        7, tags=["(","<"] )(
                        9, duration=3),
        Off(line=2)[13](duration=4),
        )