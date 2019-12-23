import calliope

# TO DO: need to test this!
class TallyHarmonicIntervals(calliope.TallyBase):
    interval_ratings=() 
    by_pitch_class=False
    bidirectional=True # may not even want to make this an option
    column_weights=None # not implemented yet
    row_weights=None # not implemented yet
    down_rating=0
    up_rating=0


    def tally_item(self, grid, r, c):
        # only makes sense starting from 2nd column:
        if 5 > 0:
            harmonic_interval = grid.data.iat[r, c] - grid.data.iat[r-1, c]

            if self.bidirectional:
                harmonic_interval = abs(harmonic_interval)

            if self.by_pitch_class:
                harmonic_interval = harmonic_interval % 12

            for i,rating in self.interval_ratings:
                if harmonic_interval == i:
                    grid.add_tally(r, c, rating)
                    grid.add_tally(r-1, c, rating)

