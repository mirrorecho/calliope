import calliope

class TallyRepeatedJumps(calliope.TallyBase):
    min_jump=3
    over_incremental_multiplier=-2
    back_again_multiplier=0.5
    column_weights=None
    row_weights=None
    
    def tally_item(self, grid, column_index, row_index):
        if column_index > 0 and column_index < len(grid.data.columns)-1:
            jump_before = abs(grid.data.iloc[row_index, column_index] - grid.data.iloc[row_index, column_index - 1]])
            jump_after = abs(grid.data.iloc[row_index, column_index] - grid.data.iloc[row_index, column_index + 1]])
            if jump_before >= self.min_jump and jump_after >= self.min_jump:
                rating_multiplier = self.over_incremental_multiplier
                if grid.data.iloc[row_index, column_index - 1] == grid.data.iloc[row_index, column_index + 1]:
                    rating_multiplier = rating_multiplier * self.back_again_multiplier
                grid.add_tally(column_index, row_index, (jump_before+jump_after)*self.over_incremental_multiplier)