import abjad
import calliope

class StackPitches(calliope.Factory):
    intervals = ( (0,12), (0,7) )
    row_machine_type = calliope.Cell

    def get_intervals(self): # can be overriden to customize
        return self.intervals

    def fabricate(self, machine, *args, **kwargs):
        pitches = self.get_pitches()
        rhythm = self.get_rhythm()
        intervals = self.get_intervals()
        initial_row = self.row_machine_type(pitches=pitches, rhythm=rhythm)
        stacked_rows = []

        for i in range(len(intervals[0])):
            my_pitches = [
                pitch + intervals[pitch_i % len(intervals)][i] 
                for pitch_i, pitch in enumerate(pitches)
                ]
            stacked_rows.append(self.row_machine_type(pitches=my_pitches, rhythm=rhythm))

        machine[:] = stacked_rows[::-1]



# ============================================================

# calliope.illustrate_me( bubble=t )
