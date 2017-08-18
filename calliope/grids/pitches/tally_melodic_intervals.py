import calliope

class TallyMelodicIntervals(calliope.TallyBase):
    def __init__(self, interval_ratings=[], over_incremental_multiplier=None, by_pitch_class=False, bidirectional=True, row_weights=None, column_weights=None, down_rating=0, up_rating=0):
        self.interval_ratings = interval_ratings
        self.by_pitch_class = by_pitch_class
        self.bidirectional = bidirectional
        self.over_incremental_multiplier = over_incremental_multiplier
        self.up_rating=up_rating
        self.down_rating=down_rating
        super().__init__(row_weights=row_weights, column_weights=column_weights)

    def tally_pitch(self, grid, row_index, column_index):
        # only makes sense starting from 2nd column:
        if column_index > 0:
            melodic_interval = grid.pitch_lines[row_index][column_index] - grid.pitch_lines[row_index][column_index-1]
            
            if self.up_rating and melodic_interval:
                grid.add_tally(row_index, column_index, self.up_rating)
            if self.down_rating and melodic_interval:
                grid.add_tally(row_index, column_index, self.down_rating)

            if self.bidirectional:
                melodic_interval = abs(melodic_interval)
            if self.by_pitch_class:
                melodic_interval = melodic_interval % 12
            for i,rating in self.interval_ratings:
                if melodic_interval == i:
                    grid.add_tally(row_index, column_index, rating)
                    grid.add_tally(row_index, column_index - 1, rating)
            # can be used to dock for big jumps
            if self.over_incremental_multiplier is not None:
                if abs(melodic_interval) > self.over_incremental_multiplier[0]:
                    over_rating = (abs(melodic_interval) - self.over_incremental_multiplier[0]) * self.over_incremental_multiplier[1]
                    grid.add_tally(row_index, column_index, over_rating)
