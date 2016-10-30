import abjad
from calliope import bubbles, tools, machines
from calliope.bubble_test_staves import MyScore

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope

class BaseLine0(bubbles.Line):
    # metrical_durations=ID1({
    #     1:((3,4),),
    #     },
    #     limit = 12
    #     )
    pass

# class Violin1(BaseLine0, bubbles.Arrange):
class Violin1(BaseLine0):
    music = bubbles.Line(""" c'1 """)

class Violin2(BaseLine0):
    music = bubbles.Line(""" c1 """)

class Viola(BaseLine0):
    music = bubbles.Line(""" c1 """)

class Cello(BaseLine0):
    music = bubbles.Line(""" c1 """)

c = Cello()

# -------------------------------

tools.illustrate_me(score_type=MyScore)