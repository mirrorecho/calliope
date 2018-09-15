import abjad
from calliope import bubbles, machines, tools
from calliope.sandbox.bubble_test_staves import MyScore

# TO DO... 
# - 1-based indices (e.g. for measures)
# - move indexed data into calliope

class MySequencedMusic(bubbles.ModuleSequence):
    modules = (
        ("bubble_test_mark_0", # "calliope.sandbox" # TO DO... WTF with the tuple?????
        	),
        ("bubble_test_mark_a",),
        # "bubble_test_mark_b",
        )

m = MySequencedMusic()
print(m.sequence())

# -------------------------------

calliope.illustrate_me(MySequencedMusic)