from abjad import *


def split(music, durations=((4,4),), cyclic=True, *args, **kwargs):
    # split notes accross bar lines (with ties) .... 
    split_durations = [Duration(d) for d in durations]
    leaves = music.select_leaves()
    result = mutate(leaves).split(split_durations, cyclic=cyclic, *args, **kwargs)
