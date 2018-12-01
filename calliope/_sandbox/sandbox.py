import abjad, abjadext, calliope


class MyScore(calliope.Score):
    class MyStaffA(calliope.Staff):
        class MyCell(calliope.Cell):
            set_pitches = (0,2,4)
            set_rhythm = (3,3,2)
    class MyStaffB(MyStaffA): pass

# print(calliope.Event._parent_types)
# print(calliope.Cell._parent_types)
# print(calliope.Phrase._parent_types)
# print(calliope.Segment._parent_types)
# print(calliope.Score.get_descendant_types())
# print(calliope.StaffGroup._parent_types)
# print(calliope.Event.get_ancestor_types())
# print(calliope.Bubble._parent_types)

s = MyScore()

print(calliope.Phrase.events)


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
# phrase_a.non_rest_events(pitch=0).setattrs(rest=True)

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

# p.cells[0,1].non_rest_events.tag(".", ">")
# p.events[2,3].non_rest_events.untag(">")

# p.non_rest_events[1].pitch = 22

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
#             selectable.non_rest_events.tag(">")

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


