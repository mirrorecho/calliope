import sys
import abjad, calliope

# class Flute(calliope.Cell):
#     music_contents = "d'4 d'4 d'4 d'4"

# class Violin(calliope.Fragment):
#     music_contents = "d'4 d'4 d'4 d'4"
#     # def music(self, **kwargs)


# fragment_a = calliope.Fragment("a1 b1 c'2 d'2")

# fragment_b = calliope.Fragment("b'1 c''1 c''2 d''2")

class Bubble1(calliope.Segment):
    class Part1(calliope.Fragment):
        music_contents = "c'4 d'4 d'4 c'4"
    class Part2(calliope.Fragment):
        music_contents = "d'4 d'4 d'4 d'4"



my_module = sys.modules[__name__]
# print(my_module
b = calliope.Bubble.from_module(my_module)
b["Bubble1"]["Part1"].illustrate_me()

