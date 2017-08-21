import calliope

class TallyMelodicIntervals(calliope.TallyBase):
    def __init__(self, 
            interval_ratings=[], 
            over_incremental_multiplier=None, 
            by_pitch_class=False, 
            bidirectional=True, 
            column_weights=None, 
            row_weights=None, 
            down_rating=0, 
            up_rating=0):
        self.interval_ratings = interval_ratings
        self.by_pitch_class = by_pitch_class
        self.bidirectional = bidirectional
        self.over_incremental_multiplier = over_incremental_multiplier
        self.up_rating=up_rating
        self.down_rating=down_rating
        super().__init__(column_weights=column_weights, row_weights=row_weights)

    def tally_item(self, grid, column_index, row_index):
        # only makes sense starting from 2nd column:
        if column_index > 0:
            melodic_interval = grid.pitch_lines[row_index][column_index] - grid.pitch_lines[row_index][column_index-1]
            
            if self.up_rating and melodic_interval:
                grid.add_tally(column_index, row_index, self.up_rating)
            if self.down_rating and melodic_interval:
                grid.add_tally(column_index, row_index, self.down_rating)

            if self.bidirectional:
                melodic_interval = abs(melodic_interval)
            if self.by_pitch_class:
                melodic_interval = melodic_interval % 12
            for i,rating in self.interval_ratings:
                if melodic_interval == i:
                    grid.add_tally(column_index, row_index, rating)
                    grid.add_tally(column_index - 1, row_index, rating)
            # can be used to dock for big jumps
            if self.over_incremental_multiplier is not None:
                if abs(melodic_interval) > self.over_incremental_multiplier[0]:
                    over_rating = (abs(melodic_interval) - self.over_incremental_multiplier[0]) * self.over_incremental_multiplier[1]
                    grid.add_tally(column_index, row_index, over_rating)
