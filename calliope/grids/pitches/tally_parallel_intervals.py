import calliope

class TallyParallelIntervals(calliope.TallyBase):
    def __init__(self, interval_ratings=[(0,-100),], by_pitch_class=True, row_weights=None, column_weights=None):
        # default is to dock off 100 points for parallel unisons/octaves
        self.interval_ratings = interval_ratings
        self.by_pitch_class = by_pitch_class
        super().__init__(row_weights=row_weights, column_weights=column_weights)

    def tally_pitch_across_lines(self, grid, row_index, column_index, across_row_index):
        # only makes sense starting from 2nd column:
        if column_index > 0:
            melodic_interval_1 = grid.pitch_lines[row_index][column_index] - grid.pitch_lines[row_index][column_index-1]
            melodic_interval_2 = grid.pitch_lines[across_row_index][column_index] - grid.pitch_lines[across_row_index][column_index-1]
            #if motion is parallel...
            if melodic_interval_1 == melodic_interval_2:
                interval = abs(grid.pitch_lines[row_index][column_index] - grid.pitch_lines[across_row_index][column_index])
                if self.by_pitch_class:
                    interval = interval % 12
                for i,rating in self.interval_ratings:
                    if interval == i:
                        grid.add_tally(row_index, column_index, rating)
                        grid.add_tally(across_row_index, column_index, rating)