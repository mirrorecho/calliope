import abjad
from calliope import bubbles, tools, machines
from calliope.sandbox.bubble_test_staves import MyScore

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope

# from test2 import *

class BaseLine0(bubbles.Line):
    # metrical_durations=ID1({
    #     1:((3,4),),
    #     },
    #     limit = 12
    #     )
    pass

# class Violin1(BaseLine0, bubbles.Arrange):
class Violin1(BaseLine0):
    music_contents = """ d'2 e'2 """

class Violin2(BaseLine0):
    music = bubbles.Line(""" c1 """)

class Viola(BaseLine0):
    music = bubbles.Line(""" c1 """)

class Cello(BaseLine0):
    music = bubbles.Line(""" c1 """)

class MyScore1(bubbles.Score):
    class Violin2(bubbles.Staff):
        pass
    # Violin2 = bubbles.Staff()
    # Violin2.instrument=abjad.instrumenttools.Violin(
    #         instrument_name="Violin 2", short_instrument_name="vln.2")
    pass


# import sys
# print(sys.modules[__name__])
# m = bubbles.ModuleBubble( module=sys.modules[__name__] )
# print(m.sequence() )

# -------------------------------

calliope.illustrate_me(score_type=MyScore1 )

