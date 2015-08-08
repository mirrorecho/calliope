# CALLIOPE DESIGN PRINCIPLES:

# KEEP IT SIMPLE! ... abjad already provides a structure, don't re-intent the wheel

# WITH THAT IN MIND, BASIC GOALS ARE:

# help create structure around non-linear musical thinking
# - - musical ideas as objects (inherit from Bubble?)
# - - use inheritance, don't cram everything into a mega-class

# a few tools to help with routine tasks
# - - templates for scores and parts

# ametrical music and systems
# - - quickly create ametrical music
# - - align all parts
# - - x/x time signature
# - - dashed bar lines
# - - boxes and arrows

# beuatifully printed music (with some fancy formatting)
# - - fonts
# - - rehearsal marks
# - - measure numbering
# - - instrument names and cues
# - - add/remove staves (and account for this in parts)

# TO DO
# - - add lilypond comments where bubbles start in voice music

from abjad import *
from bubbles import *

class SortMixin():
    # def sequence(self, *args, **kwargs):
    #     return ("line1","line2","line3","line4")
    pass

class B(SortMixin, Bubble):
    is_simultaneous = True
    line1 = Line(lambda : Container("e'4 "*4))
    line2 = Line(lambda : Container("d'4\\ff "*4))
    line3 = line2

class C(B):
    line1 = Line(lambda : Container("c'4 "*4))

    # def sequence(self, *args, **kwargs):
    #     return ("line4","line1")

b = B()
c = C()

# d = BubbleSequence((b,c,b,c))

class E(B):
    grid_sequence = (B,C)
    line4 = Line(lambda : Container("b4 "*8))

class F(E):
    grid_sequence = (E,E)
    line5 = Line(lambda : Container("a4 "*16))

class G(Bubble):
    line0 = Line(lambda : Container("a1 "*4))

class H(F,G):
    line01 = Line(lambda : Container("a'1 "*4))

class I(H)

m = H()

print(format(m.blow()))
# print(super(H))

# for a in dir(B):
#     # print(type(getattr(B,a)))
#     if isinstance(getattr(B,a), B.bubble_types):
#         print(a)

# print(dir(B))

# m = F()
# print(format(m.blow()))
# show(d.blow())

# def sequence(bubbles):
#     bubble = Bubble()
#     for i,b in enumerate(bubbles):
#         attr_name = "seq" + str(i)
#         b.order = i
#         setattr(bubble, attr_name, b)
#     return bubble


# b.b4.order=0

# show(b.blow())

# class B2(B1):
#     flute_line1 = Bubble(Container, lambda : B1_LINES.blow())
#     flute_line2 = B1.b4

# ALL_LINES = B2()


# class YoFluteStaff1(BubbleStaff):
#     flute_music = ALL_LINES.flute_line1

#     def blow_bubble(self, staff, *args, **kwargs):
#         instrument = instrumenttools.Instrument(instrument_name="Flute 1", short_instrument_name="fl.1")
#         attach(instrument, staff)

# class YoFluteStaff2(BubbleStaff):
#     flute_music = ALL_LINES.flute_line2

#     def blow_bubble(self, staff, *args, **kwargs):
#         instrument = instrumenttools.Instrument(instrument_name="Flute 1", short_instrument_name="fl.1")
#         attach(instrument, staff)

# class YoScore(BubbleScore):
#     b_music = B1()
#     flute1 = YoFluteStaff1(order=10)
#     flute2 = YoFluteStaff2(order=11)

# class B1(Bubble):
#     b2 = Bubble(Staff, lambda : "e'4 "*4, order=0)
#     b3 = Bubble(Container, lambda : "d'4\\ff "*4, order=1)
#     b4 = b3

# b = YoScore()
# print(format(b.blow()))


# b = Container("c1 c1 c1 c1")
# c = Container(b)
# s = Staff(c)
# print(format(s))


# y = Yo()
# print(format(y.blow()))

# from bubbles import Bubble
# from copy import deepcopy

# class Theme(Bubble):
#     def music(self, *args, **kwargs):
#         self.use_lines(["theme","counter","bass"])
#         self.lines["theme"].extend("\\time 2/2 c'4(\\ff d' e' f') " + " d'1 "*2 + "e'2(\\mp f'2) ")
#         self.lines["counter"].extend("c'4(\\ff d' e' f') " + "e'2(\\mp f'2) " + "d'1 "*2 )
#         self.lines["bass"].extend("\\clef bass c1\\mf d e f ")

# class Bass2(Bubble):
#     def music(self, *args, **kwargs):
#         self.use_lines(["bass2"])
#         self.lines["bass2"].extend("\\clef bass c,1\\mf " + "d,1 "*3)

# class Theme2(Bass2,Theme):
#     def music(self, *args, **kwargs):
#         mutate(self.lines["counter"]).replace(Context("d'2 "*8))
#         pass

# t1 = Theme()
# t2 = Theme2()
# t3 = Theme()

# t = Bubble.sequence([t1,t2,t3])
# print(inspect_(t).get_duration())
# s = t.score()

# print(format(s))
# print(t.lines)
# show(s)

# c = Container("c'4(\\ff d' e' f') " + "d'1 "*2 + "e'2(\\mp f'2)")
# s = Staff()
# s.extend(c)
# print(format(c))


# c = Container()
# c.is_simultaneous = True
# v1 = Context(name="voice1", music="b4 "*4)
# v2 = Context(name="voice2", music="a4 "*4)
# v3 = Context(name="voice3", music="g8 "*8)
# c.extend([v1, v2, v3])
# s1 = Staff(context_name="voice1")
# s2 = Staff(context_name="voice2")
# sg = StaffGroup([s1,s2])
# c.extend(sg)

# show(c)

# s1 = Staff()
# s2 = Staff()

# print(format(c))
# print(dir(c))

# class BubbleScore(Score):
#     pass

# class Bubble1(Bubble):
#     def music(self, *args, **kwargs):
#         self.use_voice("voice1")
#         self.use_voice("voice2")
#         self.use_voice("voice3")
#         self.use_voice("voice4")
#         self.use_voice("voice5")
#         self.use_voice("voice6")
#         self.use_voice("voice7")
#         self.use_voice("voice8")

# class Bubble2(Bubble):
#     def music(self, *args, **kwargs):
#         self.use_voice("voice9")
#         self.use_voice("voice10")
#         self.use_voice("voice11")
#         self.use_voice("voice12")
#         self.use_voice("voice13")
#         self.use_voice("voice14")
#         self.use_voice("voice15")
#         self.use_voice("voice16")

# class B2(Bubble1,Bubble2):
#     def music(self, *args, **kwargs):
#         self.lines["voice1"].extend("c'16 ( c'16 ) "*64)

#         self.lines["voice16"].extend("b'16 ( b'16 ) "*64)

# b = Bubble.sequence([B2() for i in range(4)])
# show(b)

# print(inspect_(b).get_duration())
# show(b)

# print(dir(b))

# b = B2()
# show(b)



# b = Bubble(lines=["v1","v2"])
# b[0].extend("b4 "*4)
# b[1].extend("a8 "*8)
# b.make_staves()
# print(format(b))
# show(b)