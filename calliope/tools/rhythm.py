import abjad

# TO DO... is this used?
def split(music, durations=((4,4),), cyclic=True, *args, **kwargs):
    # split notes accross bar lines (with ties) .... 
    split_durations = [abjad.Duration(d) for d in durations]
    leaves = music.select_leaves()
    result = abjad.mutate(leaves).split(split_durations, cyclic=cyclic, *args, **kwargs)

# TO DO... refactor 
def by_logical_tie_group_rests(music):
    logical_ties = abjad.select(music).logical_ties()

    return_logical_ties = []
    previous_rest_list = []

    for logical_tie in logical_ties:
        if isinstance(logical_tie[0], abjad.Rest):
            previous_rest_list += [logical_tie[0]]
        else:
            if previous_rest_list:
                return_logical_ties += [abjad.LogicalTie( previous_rest_list )]
            previous_rest_list = []
            return_logical_ties += [logical_tie]
    return return_logical_ties