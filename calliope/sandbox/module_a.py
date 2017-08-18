import abjad, calliope

class Flute(calliope.Fragment):
    music_contents = "d''4 d''4 d''4 d''4"

class Violin(calliope.Fragment):
    music_contents = "c''4 c'''4 c''4 c''4"

# fragment_a = calliope.Fragment("a1 b1 c,2 d,2", clef = "bass")

# fragment_b = calliope.Fragment("b,1 c,,1 c,,2 d,,2", clef = "bass")


calliope.illustrate_me()