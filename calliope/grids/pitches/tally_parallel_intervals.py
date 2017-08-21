import calliope

class TallyParallelIntervals(calliope.TallyBase):
    interval_ratings=((0,-100),)
    by_pitch_class=True 
    column_weights=None
    row_weights=None

    def tally_item_across_rows(self, grid, column_index, row_index, across_row_index):
        # only makes sense starting from 2nd column:
        if column_index > 0:
            melodic_interval_1 = grid.data.iloc[row_index, column_index] - grid.data.iloc[row_index, column_index - 1]
            melodic_interval_2 = grid.data.iloc[across_row_index, column_index] - grid.data.iloc[across_row_index, column_index - 1]
            #if motion is parallel...
            if melodic_interval_1 == melodic_interval_2:
                interval = abs(grid.data.iloc[row_index, column_index] - grid.data.iloc[across_row_index, column_index])
                if self.by_pitch_class:
                    interval = interval % 12
                for i,rating in self.interval_ratings:
                    if interval == i:
                        grid.add_tally(column_index, row_index, rating)
                        grid.add_tally(column_index, across_row_index, rating)