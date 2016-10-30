import abjad
from calliope import bubbles, machines, tools

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope

class MySequencedScore(bubbles.ModuleScoreSequence):
    sequence = (
        "bubble_test_mark_0",
        "bubble_test_mark_a",
        # "bubble_test_mark_b",
        )


# -------------------------------

from calliope.bubble_test_staves import MyScore
tools.illustrate_me(
		__file__, 
		lambda: MySequencedScore(),
		score_type=MyScore,
		)