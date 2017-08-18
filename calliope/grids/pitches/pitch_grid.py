import calliope

class PitchGrid(calliope.GridBase):
    def __init__(self, pitch_ranges=None, **kwargs):
        super().__init__(**kwargs)

        self.dont_touch_pitches = None # [[]] # for future use
        self.pitch_ranges = pitch_ranges # TO DO... extrapolate last entry for total # of lines/columns
        self.auto_move_into_ranges = self.pitch_ranges is not None:
        self.octave_transpositions_allowed = True


