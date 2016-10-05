import abjad
from callope import bubbles

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope

class MyScore(bubbles.BubbleScore):
    sections = (
        "bubble_test_mark_0",
        "bubble_test_mark_a",
        "bubble_test_mark_b",
        )


# -------------------------------

bubbles.illustrate_me()