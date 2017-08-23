import calliope

class TallyParallelIntervals(calliope.TallyBase):
    interval_ratings=((0,-100),)
    by_pitch_class=True 
    column_weights=None
    row_weights=None

    def tally_item_across_rows(self, grid, r, c, across_r):
        # only makes sense starting from 2nd column:
        if c > 0:
            melodic_interval_1 = grid.data.iat[r, c] - grid.data.iat[r, c - 1]
            melodic_interval_2 = grid.data.iat[across_r, c] - grid.data.iat[across_r, c - 1]
            #if motion is parallel...
            if melodic_interval_1 == melodic_interval_2:
                interval = abs(grid.data.iat[r, c] - grid.data.iat[across_r, c])
                if self.by_pitch_class:
                    interval = interval % 12
                for i,rating in self.interval_ratings:
                    if interval == i:
                        grid.add_tally(r, c, rating)
                        grid.add_tally(r, c, rating)