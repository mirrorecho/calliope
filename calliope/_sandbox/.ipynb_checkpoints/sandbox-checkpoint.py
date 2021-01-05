import abjad, calliope

c = calliope.Cell(
    name="YOYO",
    rhythm=(-0.5,-0.5,-1,-1,-1), 
    pitches=("R",2,4,"R")
    )
calliope.illustrate(c)


# class ShortScore(calliope.®actory, calliope.SegmentBlock):
#     branch_type = calliope.Segment

#     def get_branch(self, node, *args, **kwargs):
#         return node(*args, **kwargs)

#     def get_branches(self, *args, **kwargs):
#         return self

# class Arrangement(calliope.FromSelectableFactory):
#     def get_branch(self, node, *args, **kwargs):
#         return node(*args, **kwargs)

#     def get_branches(self, *args, **kwargs):
#         return self


# c.events[2].tag("\\<")
# c.events[4].tag("\\!")
# cb1 = calliope.CellBlock(
#     c(),
#     c(),
#     c(),
#     )
# cb2 = cb1(name="FOO")
# cb2.events.setattrs(pitch=4)
# cb1 = cb1 + cb2.select[1:]

# print(cb1.cells[0,1,2,3,4,5].note_events.selection_root)
# print(cb2.cells[0,1].note_events.select_from.select_from)
# print(cb2.cells[0,1].note_events.selection_root)

# calliope.illustrate(cb1)
# print(abjad.inspect(m[2]).spanners())

# c.auto_respell()
# calliope.illustrate(c)

# s = calliope.Selection()[0,1]

# c.illustrate_me()

# class MyScore(calliope.Score):

#     class CelloStaff(calliope.Staff):
#         instrument=abjad.Cello(
#             name="Cello", short_name="Vc.")

#     class PianoStaff(calliope.Piano): pass


# s = MyScore()


# # class MyLine(calliope.Line):
# class Phrase1(calliope.Phrase):
#     class CellA(calliope.Cell):
#         init_rhythm = (1,3)
#         init_pitches = (-3,4)

#     class CellB(calliope.Cell):
#         init_rhythm = (1,2,5)
#         init_pitches = (4,3,1)


# class Phrase2(Phrase1):
#     class CellB(Phrase1.CellB):
#         init_pitches = (4,3,-1)


# class Phrase3(calliope.Phrase):
#     class CellA(calliope.Cell):
#         init_rhythm = (1,3)
#         init_pitches = (-3,-6)

#     class CellB(calliope.Cell):
#         init_rhythm = (2,4)
#         init_pitches = (-5,6)


# class Phrase4(Phrase3):    
#     class CellA(Phrase3.CellA):
#         init_pitches = (4,-3)

#     class CellB(Phrase3.CellB):
#         init_pitches = (-3,-1)


# class MyLine(calliope.Line):
#     respell = "sharps"
#     class Phrase1(Phrase1): pass
#     class Phrase2(Phrase2):
#         init_bookend_rests = (1,0)
#     class Phrase3(Phrase3): pass
#         # bookend_rests = (2,0)
#     class Phrase4(Phrase4): pass

# class MyLine2(calliope.Line):
#     class Phrase1(Phrase1): 
#         init_transpose = 5

# # print(MyLine.Phrase4.CellB())


# l = MyLine()
# # print(l.rhythm)

# l.illustrate_me()

# class LineChords(calliope.ChordsFromSelectable, calliope.Line):
#     selectable = l.cells
#     respell = "sharps"

# l_chords = LineChords()

# lb = calliope.LineBlock(
#         l,
#         l_chords,
#     )
# lb.add_bookend_rests(3,0)


# e = lb[0].cells[0]
# print(sorted(e.pitch_class_set))


# import itertools
# pitch_list = [x[0] for x in itertools.groupby(l.pitches) if x[0]]
# # pitch_list_2 

# phrase_straight = calliope.Phrase(
#     pitches = pitch_list,
#     rhythm = (1,) * len(pitch_list),
#     respell="sharps"
#     )

# line_straight = calliope.Line(
#     phrase_straight,
#     phrase_straight()
#     )

# line_straight_2 = line_straight()
# line_straight_2.add_bookend_rests(2,0)

# line_straight_3 = line_straight()
# line_straight_3.add_bookend_rests(4,0)

# calliope.LineBlock(
#     line_straight(transpose=12),
#     line_straight_2,
#     line_straight_3,
#     # line_straight(bookend_rests=(1,0)) # TO DO... why won't this work???
#     ).illustrate_me()



# lb.illustrate_me()

# def fifths_away(pitch_number, from_pitch=0):
#     return ((pitch_number-from_pitch) * 7) % 12

# class ChordChomp(calliope.Transform):
#     def transform(self, selectable):
#         for event in selectable.note_events:
#             pitches = event.pi


# print(fifths_away(7,2))

# l.illustrate_me()

# s["cello_staff"].append(calliope.Cell(pitches=[0,2], rhythm=[3,5]))

# s.staves["piano1"].append(calliope.Cell(pitches=[0,2], rhythm=[3,5]))
# s.staves["piano2"].append(calliope.Cell(pitches=[0,2], rhythm=[3,5]))

# s.illustrate_me()


    # class MyStaffA(calliope.Staff):
    #     class MyCell(calliope.Cell): 
    #         set_pitches = (None,2,4)
    #         set_rhythm = (3,3,2)
    #         # class MyCellSub(calliope.Cell): 
    #         #     set_pitches = (5,2,4)
    #         #     set_rhythm = (1,1,1)
    #     class MyCell2(calliope.Cell): 
    #         set_pitches = (6,2,4)
    #         set_rhythm = (3,3,2)
    # class MyStaffB(MyStaffA): 
    #     class MyCell2(calliope.Cell): 
    #         set_pitches = (6,2,4)
    #         set_rhythm = (2,2,4)

# print(calliope.Event._parent_types)
# print(calliope.Cell._parent_types)
# print(calliope.Phrase._parent_types)
# print(calliope.Segment._parent_types)
# print(calliope.Score.get_descendant_types())
# print(calliope.StaffGroup._parent_types)
# print(calliope.Event.get_ancestor_types())
# print(calliope.Bubble._parent_types)

# print(calliope.SELECTION_COUNTER, "START")

# s = MyScore()

# print(calliope.SELECTION_COUNTER, "AFTER CREATING SCORE OBJECT")

# # s.staves(0,1).events[3].tag(">")

# s.staves[1].events[1,3].tag(">")

# print(calliope.SELECTION_COUNTER, "AFTER TAGGING ACCENT")

# # c3 = calliope.Cell("my_cell3", pitches=(0,2), rhythm=(2,2))

# print(calliope.SELECTION_COUNTER, "AFTER CREATING NEW CELL")

# s["my_staff_a"].append(c3)

# print(calliope.SELECTION_COUNTER, "AFTER ADDING NEW CELL")

# s.illustrate_me()

# print(calliope.SELECTION_COUNTER, "AFTER ILLUSTRATING")

# print(s.staves_YO)
# print(s.staves_YA)

# print(s.staves[0].select_cells)

# print(s.note_events)

# s2 = calliope.Score()

# print(s._parent_types is s2._parent_types)

# s.staves[1].append(calliope.Cell(rhythm=(2,2), pitches=(5,4)))

# # c = calliope.Cell(
# #     pitches=(0,2,6),
# #     rhythm=(3,3,2)
# #     )

# s.illustrate_me()

# class MyScore(calliope.Score):
#     class Violins(calliope.StaffGroup):
#         class Violin1Staff(calliope.Staff):
#             instrument=abjad.Violin(
#                 name="Violin 1", short_name="vln.1")
#             class ViolinMusicA(calliope.Line):
#                 is_simultaneous=False
#                 class MyCell(calliope.Cell):
#                     set_rhythm=(1,1,1,5)
#                     set_pitches=(0,2,3,5)

#         class Violin2Staff(calliope.Staff):
#             instrument=abjad.Violin(
#                 name="Violin 2", short_name="vln.2")
#             class ViolinMusicA(calliope.Bubble):
#                 is_simultaneous=False
#                 music_contents="c'1 b2 b2"

# # MyScore().illustrate_me()
# s = MyScore()
# print(s.cells)

# s = calliope.Score(
#     calliope.Staff(
#         calliope.Bubble(is_simultaneous=False, music_contents="c'1 b2 b2"),
#         calliope.Bubble(is_simultaneous=False, music_contents="b2 b2 c'1 "),
#         ),
#     calliope.Staff(
#         calliope.Bubble(is_simultaneous=False, music_contents="a2 a2 d'1"),
#         calliope.Bubble(is_simultaneous=False, music_contents="d'1 a2 a2"),
#         ),
#     )

# print(s.staves)

# s.illustrate_me()

# class MyTwig(calliope.Tree):
#     child_types = ()
#     select_property = "twigs"

# class MyBranch(calliope.Tree):

#     select_property = "branches"

# MyBranch.child_types = (MyTwig, MyBranch)

# class MyTrunk(calliope.Tree):
#     child_types = (MyBranch,)
#     select_property = "trunks"

# class MyTree(calliope.Tree):
#     child_types = (MyTrunk,)

# # MyTwig.child_types=(MyTrunk,)



# set_select_properties(MyTree)




# t = MyTree(
#     MyTwig(name="twig_bad"), # TO DO: this should throw a warning
#     MyTrunk(name="trunk1",
#         ),
#     MyTrunk(name="trunk2",
#         ),
#     )

# print(t.trunks["trunk1"])


# class Arrange(calliope.Transform):
#     arrange_from = None

#     def __init__(self, arrange_from=None, **kwargs):
#         self.arrange_from = arrange_from or self.arrange_from
#         super().__init__(**kwargs) 

#     # def get_detination_branches(self, selectable):
#     #     if self.detination_branch_names:
#     #         return selectable[*self.detination_branch_names]
#     #      else: 
#     #         selectable.select

#     def transform(self, selectable, **kwargs):
#         for name,value in kwargs.items():
#             selectable[name].append(self.arrange_from[value]())


# class PhraseA(calliope.Phrase):
#     class CellA1(calliope.Cell):
#         set_rhythm=(3,3,3,3) 
#         set_pitches=(4,7,5,3)
#     class CellA2(calliope.Cell):
#         set_rhythm=(2,4,4,2)
#         set_pitches=(0,2,0,2)

# class PhraseB(calliope.Phrase):
#     class CellB1(PhraseA.CellA1):
#         set_rhythm=(2,2,2,2) 
#     class CellB2(PhraseA.CellA2):
#         set_rhythm=(2,2,2,2) 


# phrase_block = calliope.PhraseBlock(
#     PhraseA(),
#     PhraseB(),
#     )


# class CloselyScore(calliope.Score):
#     stylesheets=("../../stylesheets/score.ily",)
#     class Violin(calliope.Staff):
#         instrument=abjad.Violin(
#             name="Violin", short_name="vln.")

#     class Cello(calliope.Staff):
#         instrument=abjad.Cello(
#             name="Cello", short_name="vc.")
#         clef="bass"

# closely_score = CloselyScore()

# phrase_a = PhraseA()
# phrase_a.note_events(pitch=0).setattrs(rest=True)

# arrange_block = Arrange(phrase_block)
# arrange_block(closely_score, Violin=0, Cello=1)

# # closely_score["Violin"].append(calliope.Cell(rhythm=(1,1,1,1)))
# # closely_score["Cello"].append(calliope.Cell(rhythm=(2,1), pitches=(4,2)))
# # calliope.illustrate_me(bubble=cs, score_type=CloselyScore)
# # calliope.illustrate_me(bubble=closely_score)

# print(phrase_block.cells[1:].events)
# """

"""
<<Score>>
( <<StaffGroup>> )(...)
{Staff}
( {Voice} ) ( <<VoiceBlock>> )
{Section} <<SectionBlock>>
( {Line} ) <<LineBlock>>
( {Cell} )(...) <<CellBlock>>
Event
LogicalTie
(Leaf) (psuedo) [Chord] (psuedo)
"""
# """

# my_score.sections["a"].staves["violin"].lines[2]

# my_score.sections["a"].staves["violin"].lines[2]


# phrase_a.illustrate_me()
# closely_score.illustrate_me()


# p = PhraseA()
# AccentMe()(p["CellA2"])
# p.illustrate_me()


# class MyTree(calliope.Tree):
#     class SubTreeYo(calliope.Tree):
#         pass
#     class SubTree(calliope.Tree):
#         pass
#     class SubTree2(calliope.Tree):
#         pass



# print(MyTree.class_sequence())


# c = calliope.Cell(
#     rhythm=(1,1,1,1,3,2), 
#     pitches=(2,0,None,7,None,6)
#     )

# cb = calliope.CellBlock(
#     calliope.Cell("violin1",
#         rhythm=(1,1,1,1,3,2), 
#         pitches=(4,0,None,7,None,6)        
#         ),
#     calliope.Cell("violin2",
#         rhythm=(1,1,1,1,3,2), 
#         pitches=(2,0,None,7,None,6)        
#         ),
#     )

# THESE ALL WORK OK:
# calliope.illustrate_me(bubble=cb)
# cb.illustrate_me()
# c.illustrate_me()

# TO DO: why doesn't this work?????!!!!
# calliope.illustrate_me(bubble=c)


 
# class MyFactory(calliope.Factory):
#     factory_pitches=(0,1,2)
#     factory_rhythm=(2,2,4)

#     def get_pitches(self):
#         return [f + 12 for f in self.factory_pitches]

# f = calliope.Cell(
#     factory = MyFactory()
#     )
# f.illustrate_me()


# class MyStack(calliope.StackPitches, calliope.CellBlock):
#     factory_pitches = (0,2,5,3,7,)
#     factory_rhythm = (1,2,1,3,1)
#     intervals = ( (0,12), (7,8) )

#     class Add0Pitch(calliope.AddConstantPitch): 
#         pitch = 0

# c = MyStack()
# print(c.select)
# c.illustrate_me()




# # from calliope.sandbox import module_0, module_a

# pb = calliope.PhraseBlock(
#     PhraseI("yo1"), 
#     PhraseI("yo2", metrical_offset=0)
#     )

# p = PhraseI()

# for l in p.leaves:
#     print(l)

# p.cells[0,1].note_events.tag(".", ">")
# p.events[2,3].note_events.untag(">")

# p.note_events[1].pitch = 22

# TO DO: why do the below behave differently?... should address:
# calliope.illustrate_me(bubble=pb)
# pb.illustrate_me()

# print(dir(m.root_node))

# RESTS MUST ONLY TAKE UP ONE NODE
# NOTES MUST CAN TAKE UP MULTIPLE... BUT ONLY AT SAME LEVEL WITH SAME PARENT
# BEAMS SPECIFY LEVEL

# m = abjad.Meter('''(4/4 (
#         (2/4 (
#             1/4
#             1/4
#             )
#         )
#         (2/4 (
#             1/4
#             1/4
#             )
#         )
#     ))''')

# t = TestMe()
# t.events[0,1,3,4].tag("YO")
# print(t.events[0].tags)
# print(t.events[1].tags)

# r = abjad.Rest(abjad.Duration(1,4))
# # r = abjad.Note("c4")
# mark = abjad.Markup("YOYOYO", direction=Up)
# abjad.attach(mark, r)
# abjad.show(r)

# c1 = calliope.Cell(
#     calliope.Cell(rhythm=(1,1,1,1,1), pitches=(0,-1,0,-1,2,3)),
#     calliope.CustomCell(beats=4, music_contents="\\times 4/5 { f4 g a b c' }"),
#     calliope.Cell(rhythm=(1,1,1,1,3), pitches=(0,-1,0,-1)),
#     )

# print(c1.get_signed_ticks_list())
# print(c1[1].get_signed_ticks_list())

# print(c1.beats)
# c1.illustrate_me()

# t = abjad.Tuplet((2, 3),
#     "b8 b8 b8"
#     )
# # abjad.show(t)
# print(dir(t))


# class TupletCell(calliope.ContainerCell):
#     multiplier = (2,3)
#     container_type = abjad.Tuplet

#     @property
#     def ticks(self):
#         tuplet_ticks = sum([l.ticks for l in self.logical_ties])
#         return int(tuplet_ticks * self.multiplier[0] / self.multiplier[1])

#     def music(self, **kwargs):
#         my_music = self.container_type(multiplier=self.multiplier, music=self.get_rhythm_music(**kwargs), **kwargs)
#         self.process_rhythm_music(my_music, **kwargs)
#         return my_music

# t = TupletCell(rhythm=(1,1,1,1,1), multiplier=(4,5))
# p = calliope.Phrase(
#     calliope.Cell(rhythm=(2,2)),
#     t,
#     calliope.Cell(rhythm=(2,2)),
#     )


# class SomeFactory(calliope.Factory):

#     def fabricate(self, machine, *args, **kwargs):
#         machine.extend([calliope.Cell(rhythm=(2,2)), calliope.Cell(rhythm=(4,4))])

# # TWO WAYS TO USE FACTORIES (class vs instance)
# # 1)
# class MyPhrase(SomeFactory, calliope.Phrase): pass
# p = MyPhrase()
# # 2)
# p = calliope.Phrase(factory=SomeFactory())




# class PhraseA(calliope.Phrase):
#     class CellA(calliope.Cell):
#         set_rhythm=(3,3)
#         set_pitches=(0,2)
#     class CellA(calliope.Cell):
#         set_rhythm=(2,4)
#         set_pitches=(4,5)

#     class AccentMe(calliope.Transform):
#         def transform(self, selectable, **kwargs):
#             selectable.note_events.tag(">")

# p = PhraseA()
# selection = p.events(pitch__gt=0)

# pc = calliope.Cell(
#     factory=calliope.CopyEventsFactory(selection=selection)
#     )

# print(pc.name, "YA")


# p_args_a = calliope.Phrase(
#         calliope.RestEvent(beats=4),
#         calliope.Cell(rhythm=(-1,1,-1,1)),
#         calliope.Cell(rhythm=(1,0.5,0.5,2)),
#         calliope.Cell(rhythm=(-1,1,-1,1), pitches=(2,2,2,None)),
#         )
# # p_args_a.ly()
# # p_args_a.pitches= [0,1,2,3,4,5,6,7,8,9,None,None,12]
# # p_args_a.events[3].rest = True

# p_args_a.pitches=(0,None,4)*4 + (2,)
# print(p_args_a.ly())

# print(PhraseANew().pitches)

# class FragmentA(calliope.Fragment):
#     music_contents = "e'2. R2."
#     time_signature = (3,4)
#     clef = "bass"

# class FragmentB(calliope.Fragment):
#     music_contents = "cs'2. d'2 r4 b2."
#     bar_line = "!"


# f = calliope.Fragment(FragmentA(), FragmentB())

# print(format(f.music()))

# f.illustrate_me()


