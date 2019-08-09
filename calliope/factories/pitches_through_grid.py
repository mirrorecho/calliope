import numpy as np
import pandas as pd

import calliope

class PitchesThroughGrid(calliope.FromSelectableFactory, calliope.PitchGrid):
    """
    for blocks where each row has the same number of notes with no chords... 
    """

    # def __init__(self, selectable=None, *args, **kwargs):
    #     super().__init__(selectable=selectable, *args, **kwargs)

    def get_start_data(self):
        return pd.DataFrame.from_records([l.pitches for l in self.selectable])

    def get_branch(self, node, index, *args, **kwargs):
        return node(pitches=self.data.iloc[index], *args, **kwargs)

    # TO DO MAYBE: index always passed to branch
    def get_branches(self, *args, **kwargs):
        return [self.get_branch(n, i, *args, **kwargs) for i, n in enumerate(self.selectable)]

    def update_rearranged(self):
        print("HOLLY COW")
        for i,l in enumerate(self):
            l.pitches = self.data.iloc[i]
