import calliope

class TallyMelodicIntervals(calliope.TallyBase):
    interval_ratings=() 
    over_incremental_multiplier=None # e.g. (12, 10)
    by_pitch_class=False
    bidirectional=True
    column_weights=None
    row_weights=None
    down_rating=0
    up_rating=0


    def tally_item(self, grid, r, c):
        # only makes sense starting from 2nd column:
        if c > 0:
            melodic_interval = grid.data.iat[r, c] - grid.data.iat[r, c - 1]
            
            if self.up_rating and melodic_interval > 0:
                grid.add_tally(r, c, self.up_rating)
            if self.down_rating and melodic_interval < 0:
                grid.add_tally(r, c, self.down_rating)

            if self.bidirectional:
                melodic_interval = abs(melodic_interval)

            if self.by_pitch_class:
                melodic_interval = melodic_interval % 12

            for i,rating in self.interval_ratings:
                if melodic_interval == i:
                    grid.add_tally(r, c, rating)
                    grid.add_tally(r, c - 1, rating)

            # can be used to dock for big jumps
            if self.over_incremental_multiplier:
                if abs(melodic_interval) > self.over_incremental_multiplier[0]:
                    over_rating = (abs(melodic_interval) - self.over_incremental_multiplier[0]) * self.over_incremental_multiplier[1]
                    grid.add_tally(r, c, over_rating)
