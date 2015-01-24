from abjad import *
from calliope.tools import pitches_from_intervals

# QUESTION.... IS THERE ALREADY SOMETHING BUILT INTO ABJAD TO DO THIS KIND OF THING?
class IntervalRepeatCell:

    # intervals = []
    # current_start_pitch = 0

    def __init__(self, intervals=[], start_pitch= 0, pitch_range = None):
        self.intervals = intervals
        self.start_pitch = start_pitch
        self.pitch_range = pitch_range
        self.make_pitches()

    def make_pitches(self, pitch_range = None):

        # the last interval is for the start of the next repetition, so get pitches for intervals before that:
        self.pitches = pitches_from_intervals(self.intervals[:-1])

        if self.pitch_range is not None:
            self.pitches = pitchtools.transpose_pitch_expr_into_pitch_range(self.pitches, self.pitch_range)

    # TO DO... make leaves (e.g. use rests/skips)
    def next(self, pitch_range = None):
        # the new start pitch (for the next go-around) is just the sum of all the intervals:
        self.start_pitch += sum(self.intervals)
        self.make_pitches()
        
