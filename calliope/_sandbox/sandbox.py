import abjad, calliope

c = calliope.Event(beats=2, pitch=2)
# c.illustrate_me()

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


