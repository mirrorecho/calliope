import calliope

class TallyRepeatedJumps(calliope.TallyBase):
    def __init__(self, 
            min_jump=3, over_
            incremental_multiplier=-2, 
            back_again_multiplier=0.5, 
            row_weights=None, 
            column_weights=None):
        self.min_jump=3
        self.back_again_multiplier = back_again_multiplier # this let's us say that jumps back to the same pitch not as bad
        self.over_incremental_multiplier = over_incremental_multiplier
        super().__init__(row_weights=row_weights, column_weights=column_weights)
    
    def tally_pitch(self, grid, row_index, column_index):
        if column_index > 0 and column_index < grid.num_columns-1:
            jump_1 = abs(grid.pitch_lines[row_index][column_index] - grid.pitch_lines[row_index][column_index-1])
            jump_2 = abs(grid.pitch_lines[row_index][column_index] - grid.pitch_lines[row_index][column_index+1])
            if jump_1 >= self.min_jump and jump_2 >= self.min_jump:
                rating_multiplier = self.over_incremental_multiplier
                if grid.pitch_lines[row_index][column_index-1] == grid.pitch_lines[row_index][column_index+1]:
                    rating_multiplier = rating_multiplier * self.back_again_multiplier
                grid.add_tally(row_index, column_index, (jump_1+jump_2)*self.over_incremental_multiplier)