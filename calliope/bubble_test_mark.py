from callope import bubbles

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope


class BaseLine(machines.DataLine):
    metrical_durations=ID1( 
        1:((3,4),),
        limit = 12
        )

class Violin1(BaseLine, bubbles.Arrange):
    music = bubbles.Line()

class Violin2(BaseLine, bubbles.Arrange):
    music = bubbles.Line()

class Viola(BaseLine, bubbles.Arrange):
    music = bubbles.Line()

class Cello(BaseLine, bubbles.Arrange):
    music = bubbles.Line()

# -------------------------------

bubbles.illustrate_me()