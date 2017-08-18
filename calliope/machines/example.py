import inspect, abjad
import calliope

c1 = calliope.Cell(name="mycell", pitches=(-2,-4,-5), rhythm=(2,1,1))
c2 = calliope.Cell(
	calliope.Event(beats=2, pitch=3), 
	calliope.Event(beats=2, pitch=4), 
	name="mycell2")

p1 = calliope.Phrase(c1, c2, name="phrase1")

calliope.illustrate_me(bubble=calliope.Bubble(p1) )


# class InventoryBasedCell(calliope.Cell):
#     pitch_inventory = None # set to calliope.SeriesCollection  in sub-classes
#     rhythm_inventory = None # ditto

#     def set_data(self, *args, **kwargs):
#         # thought... should this just happen on the init???
#         # TO DO: add in pitch processing
#         if self.rhythm and self.rhythm in self.rhythm_inventory:
#             for beats in self.rhythm_inventory[self.rhythm]:
#                 child_event = self.branch()
#                 child_event.set_data(beats=beats, **kwargs)

# class CopperCell(InventoryBasedCell):
#     pitch_inventory = calliope.SeriesCollection({
        # "hi": ( 2, 0,-1),
#         "low": (-5,-3,-1),
#         "mid": (-3, 0,-1),
#         })
#     rhythm_inventory = calliope.SeriesCollection({
#         "medium": (2, 1, 1),
#         "short": (1, 1, 1),
#         "long": (4, 1, 1),
#       })

# class SimplePhrase(calliope.Phrase):
#     cella = ManualCell()
#     cellb = ManualCell()
#     cellb.event1a = calliope.Event(beats=1, rest=True)

# # print(c.sequence())
# # print(c.__dict__)
# # print(c.__class__.__dict__)
# s = SimplePhrase()
# sc = bubbles.AutoScore(s)
# print(sc.sequence())
# # calliope.illustrate_me( bubble=s )




# CELL_A = calliope.Cell(rhythm=(1,1,2), pitches=(-3,-2,0))


# import copy
# from calliope import structures, machines
# X = calliope.XDefinition

# class CopperPhrase(InventoryBasedPhrase):
#     pitch_cell_inventory = calliope.SeriesCollection({
#         "hi": ( 2, 0,-1),
#         "low": (-5,-3,-1),
#         "mid": (-3, 0,-1),
#         })
#     rhythm_cell_inventory = calliope.SeriesCollection({
#         "medium": (2, 1, 1),
#         "short": (1, 1, 1),
#         "long": (4, 1, 1),
#     })

 
# class PhraseA(CopperPhrase):
#     cell_a = Cell(pitches="hi", rhythm="medium")
#     cell_b = Cell(pitches="low", rhythm="medium")

# class PhraseB(PhraseA):
#     cell_b = Cell(pitches="mid", rhythm="medium")
#     cell_c = Cell(pitches="mid", rhythm="short")

# class PhraseC(PhraseA):
#     cell_a = Cell(pitches="hi", rhythm="long")

# class PhraseD(PhraseA):
#     cell_c = Cell(pitches="mid", rhythm="short")

#     def set_data(self):



# class LineMixin(object): # basic attributes, such as starting time signature, rehearsal mark, etc.
#     metrical_durations = calliope.Series(default=((4,4),), limit=12)
#     # tempo_units_per_minute = 48 # TO DO... tempo indication makes everything SLOW... WHY?????
#     # tempo_text = "Slow"
#     tempo_command = '\\note #"4" #1 = 48'
#     # tempo_units_per_minute = 48
#     time_signature = (4,4)



# class CellA():
#     name="top"
#     pitches="hi"
#     rhytms="medium"

# CELL_B = Cell("mid", pitches="mid", rhythm="medium")

# CELL_C = Cell("bottom", pitches="mid", rhythm="medium")

# class CellBlockA(calliope.CellBlock):
#     name = "block_a"
#     top = CellA()
#     mid = CELL_B
#     bottom = Cell(pitches="mid", rhythm="medium")

# CELL_BLOCK_B = calliope.CellBlock(
#     CELL_B, 
#     CELL_C
#     )

# class PhraseBlockA(calliope.PhraseBlock):
#     phrase1 = Phrase( CellBlockA(), CellA("top") )
#     phrase2 = Phrase( CELL_C * 2 )

# PHRASE_BLOCK_B = calliope.PhraseBlock(
#     top = Phrase
#     )

# LINE_1 = calliope.PitchedMachine(
#     Phrase(
#         (   CellA(),
#             CellB(),
#         ),(
#             CellB(),
#             Cell(pitches="mid", rhythm="short")
#         )
#         CellB(),
#         ),
#     Phrase(
#         CellA(),
#         CellB(),
#         Cell(pitches="mid", rhythm="short")
#         ),
#     phrase_b = CopperPhrase(
#         cell_a = Cell(pitches="hi", rhythm="medium"),
#         cell_b = Cell(pitches="mid", rhythm="medium"),
#         cell_c = Cell(pitches="mid", rhythm="short"),
#         ),
#     phrase_c = CopperPhrase(
#         cell_a = Cell(pitches="hi", rhythm="long"),
#         ),
#     phrase_c = CopperPhrase(
#         cell_a = Cell(pitches="hi", rhythm="medium"),
#         cell_b = Cell(pitches="low", rhythm="medium"),
#         cell_a = Cell(pitches="mid", rhythm="long"),
#         ),
#     )

# class BaseLine(LineMixin, calliope.PitchedMachine):
#     phrase_a = PhraseA()
#     phrase_b = PhraseB()
#     phrase_b2 = PhraseB()
#     phrase_c = PhraseC()
#     phrase_d = PhraseD()

#     rhythm_initial_silence = 1
#     rhythm_times = 1

#     slow_p1 = calliope.ScaleRhythms(
#         2, 
#         phrase_a=1, 
#         phrase_b=X(cell_a=4) 
#         )


# class PulsedEnding(calliope.PulseRhythms):
#     scope = X(phrase_d = X(0.5, cell_c=0.25))

#     def set_logical_tie(self, logical_tie, **kwargs):


# class LineRhythmsDeveloped1(calliope.RhythmsMultiplied, CopperLine):
#     slow_p1 = calliope.ScaleRhythms(
#         2, 
#         phrase_a=1, 
#         phrase_b=X(cell_a=4) 
#         )
#     break_phrases =  calliope.ExtendLongNotes(
#         phrase_a=X(cell_a=2)
#         )
#     pulse_ending = calliope.PulseRhythms(
#         phrase_d=X(0.5, cell_c=0.25)
#         )
#     up_fifths = calliope.DisplacePitches(
#         phrase_b=X(cell_b=7)
#         )

#     def develop(self, *args, **kwargs):
#         self.up_fifths()
#         self.slow_p1()
#         self.slow_p1() 



# # TO DO .... add ArrangedLine to bubbles
# class MusicBase(LineMixin, bubbles.ArrangedLine):
#     unarranged = None # this is what to output if line is not arranged
#     line0 = BaseLine()
#     line1 = LineRhythmsDeveloped1()
#     line2 = LineRhythmsDeveloped2()
#     # show_data_attr="depthwise_index"
#     respell="sharps"


# class Flute1(MusicBase):

#     f1 = Fragment(
#             "line1", 
#             ("phrase_b", ("cell_a", "cell_c") ),
#             ("phrase_c", ),
#             )[2:20]

#     f2 = Fragment(
#             "line2", 
#             )[2:8]

#     f3 = 


#     bite1 = Arrange(
#         Off("line0", phrase)[3:4](),
#         Off(line=2)[7:10](
#                         7, tags=["(","<"] )(
#                         9, duration=3),
#         Off(line=2)[13](duration=4),
#         )



