import abjad
from calliope import tools, bubbles, machines

class MyShortScore(bubbles.Bubble):
    is_simultaneous = True

    line1 = machines.Line(
        machines.Event(pitch=0, beats=1),
        machines.Event(pitch=0, beats=1),
        )
    line2 = machines.Line(
        machines.Event(pitch=2, beats=1),
        machines.Event(pitch=2, beats=1),
        )
    line3 = machines.Line(
        machines.Event(pitch=4, beats=1),
        machines.Event(pitch=4, beats=1),
        )
    line4 = machines.Line(
        machines.Event(pitch=5, beats=1),
        machines.Event(pitch=5, beats=1),
        )

SCORE = MyShortScore()

my_map = bubbles.Mapping() \
    ["line1"][0, 2]() \
    ["line3"]() \

MY_PHRASE = SCORE.map_to(machines.Phrase, my_map
    )


print(MY_PHRASE.ly)

# c = b.map_to(bubbles.Bubble, bubbles.Mapping()
#     [0]()
#     [2]()
#     )

# print(b.ly)