import abjad
import calliope

class StackPitches(calliope.Factory):
    intervals = ( (0,12), (0,7) )

    def get_intervals(self): # can be overriden to customize
        return self.intervals

    def get_branches(self, *args, **kwargs):
        intervals = self.get_intervals()

        my_branches = []

        initial_branch = self.get_branch(*args, **kwargs)
        initial_pitches = initial_branch.pitches

        for i in range(len(intervals[0])):
            my_pitches = [
                pitch + intervals[pitch_i % len(intervals)][i] if pitch is not None else None
                for pitch_i, pitch in enumerate(initial_pitches)
                ]
            my_new_branch = initial_branch(pitches=my_pitches)
            my_branches.insert(0, my_new_branch)

        return my_branches




# ============================================================

# calliope.illustrate_me( bubble=t )
