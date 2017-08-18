import abjad
from calliope import bubbles, tools, machines
import bubble_test_mark_0

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope


# class BaseLineA(calliope.DataLine):
# class BaseLineA(bubble_test_mark_0.BaseLine0):
class BaseLineA(bubble_test_mark_0.BaseLine0):
    # metrical_durations=ID1( {
    #     1:((3,4),),
    #     },
    #     limit = 12
    #     )
    pass

class Violin1(BaseLineA):
    music = bubbles.Line("d2 d2")

# class Violin2(BaseLineA, bubbles.Arrange):
#     music = bubbles.Line()

# class Viola(BaseLineA, bubbles.Arrange):
#     music = bubbles.Line()

# class Cello(BaseLineA, bubbles.Arrange):
#     music = bubbles.Line()

# -------------------------------

calliope.illustrate_me()