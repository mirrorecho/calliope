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

from abjad import *
from bubbles import Bubble
from copy import deepcopy

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

def get_fa():
    print("SETTING:fa")
    return "fa"

class Ta:
    @classmethod
    def tata(cls):
        print(cls)

    class_material = {}
    class_material["yo"] = get_fa()

    def __init__(self):
        self.material = {}
        self.material.update(self.class_material)


class Ta1(Ta):
    tata()
    class_material = deepcopy(Ta.class_material)
    class_material["yo1"] = "ta1"

class Ta2(Ta):
    class_material = deepcopy(Ta.class_material)
    class_material["yo2"] = "ta2"


class TaDown(Ta1,Ta2):
    pass

t1 = TaDown()
t2 = TaDown()
t = Ta()

print(t.material)
print(t1.material)
print(t2.material)





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
#         self.voices["voice1"].extend("c'16 ( c'16 ) "*64)

#         self.voices["voice16"].extend("b'16 ( b'16 ) "*64)

# b = Bubble.sequence([B2() for i in range(4)])
# show(b)

# print(inspect_(b).get_duration())
# show(b)

# print(dir(b))

# b = B2()
# show(b)



# b = Bubble(voices=["v1","v2"])
# b[0].extend("b4 "*4)
# b[1].extend("a8 "*8)
# b.make_staves()
# print(format(b))
# show(b)