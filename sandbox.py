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

class BubbleScore(Score):
    pass

class Bubble(Container):
    def __init__(self, 
            name="a-bubble", 
            *args, **kwargs
            ):
        super().__init__(*args, **kwargs)
        self.name=name
        self.is_simultaneous = True

        self.voices = {} # necessary?
        self.material = {}

        # a little hacky... but works well... this calls the music method on every base class
        for c in reversed( type(self).mro()[:-2] ):
            # print(c)
            if hasattr(c, "music"):
                c.music(self, *args, **kwargs)
                pass

    @classmethod
    def sequence(cls, bubbles=[], name="a-sequence"):
        print(cls)
        mybubble = cls(name=name)
        # TO DO... FIX LENGTHS
        for b in bubbles:
            mybubble.use_voices(b.voices)
        for b in bubbles:
            for n, v in b.voices.items():
                mybubble.voices[n].extend(v)
        return mybubble


    def music(self, *args, **kwargs):
        """
        default hook...
        """
        pass

    def use_voices(self, names, *args, **kwargs):
        for v in names:
            self.use_voice(v)

    def use_voice(self, name, *args, **kwargs):
        if name not in self.voices:
            voice = Context(name=name, context_name="Voice", *args, **kwargs)
            self.append(voice)
            self.voices[name] = voice

    def load_material(self):
        # TO DO... PULL MATERIAL INTO DICT FROM JSON
        pass

    # TO DO... make this better
    def make_staves(self):
        for i, v in enumerate(self.voices):
            staff = Staff(name=v+"-staff")
            staff_voice = Context(name=v, context_name="Voice")
            staff.append(staff_voice)
            self.insert(i, staff)



class Bubble1(Bubble):
    def music(self, *args, **kwargs):
        self.use_voice("voice1")
        self.use_voice("voice2")
        self.use_voice("voice3")
        self.use_voice("voice4")
        self.use_voice("voice5")
        self.use_voice("voice6")
        self.use_voice("voice7")
        self.use_voice("voice8")

class Bubble2(Bubble):
    def music(self, *args, **kwargs):
        self.use_voice("voice9")
        self.use_voice("voice10")
        self.use_voice("voice11")
        self.use_voice("voice12")
        self.use_voice("voice13")
        self.use_voice("voice14")
        self.use_voice("voice15")
        self.use_voice("voice16")

class B2(Bubble1,Bubble2):
    def music(self, *args, **kwargs):
        self.voices["voice1"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice2"].extend("b'16 ( b'16 ) "*64)
        self.voices["voice3"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice4"].extend("b'16 ( b'16 ) "*64)
        self.voices["voice5"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice6"].extend("b'16 ( b'16 ) "*64)
        self.voices["voice7"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice8"].extend("b'16 ( b'16 ) "*64)
        self.voices["voice9"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice10"].extend("b'16 ( b'16 ) "*64)
        self.voices["voice11"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice12"].extend("b'16 ( b'16 ) "*64)
        self.voices["voice13"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice14"].extend("b'16 ( b'16 ) "*64)
        self.voices["voice15"].extend("c'16 ( c'16 ) "*64)
        self.voices["voice16"].extend("b'16 ( b'16 ) "*64)

b = Bubble.sequence([B2() for i in range(40)])
show(b)

print(inspect_(b).get_duration())
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