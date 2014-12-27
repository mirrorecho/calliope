from abjad import *

# QUESTION.... IS THERE ALREADY SOMETHING BUILT INTO ABJAD TO DO THIS KIND OF THING?
class IntervalRepeatCell:

    # intervals = []
    # current_start_pitch = 0

    def __init__(self, intervals=[], start_pitch= 0, pitch_range = None):
        self.intervals = intervals
        self.current_start_pitch = start_pitch
        self.pitch_range = pitch_range
        self.make_pitches()

    def make_pitches(self, pitch_range = None):
        # a cute way to convert the list of intervals to a list of relative pitches (always starting on 0)
        relative_pitches = [sum(self.intervals[:x]) for x in range(len(self.intervals))]
        
        #now create absolute pitches from relative pitches
        pitch_numbers = [pitchtools.NumberedPitch(self.current_start_pitch).pitch_number + x for x in relative_pitches]

        if self.pitch_range is not None:
            pitch_numbers = pitchtools.transpose_pitch_expr_into_pitch_range(pitch_numbers, self.pitch_range)

        self.pitches = pitch_numbers

    # TO DO... make leaves (e.g. use rests/skips)
    def next(self, pitch_range = None):
        # the new start pitch (for the next go-around) is just the sum of all the intervals:
        self.current_start_pitch += sum(self.intervals)
        self.make_pitches()
        
    def make_notes(self, durations):
        notes = scoretools.make_notes(self.pitches, durations, decrease_durations_monotonically=False)

        return notes