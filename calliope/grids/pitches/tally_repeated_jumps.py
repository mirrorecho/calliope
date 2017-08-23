import calliope

class TallyRepeatedJumps(calliope.TallyBase):
    min_jump=3
    over_incremental_multiplier=-2
    back_again_multiplier=0.5
    column_weights=None
    row_weights=None
    
    def tally_item(self, grid, r, c):
        if 0 < c < len(grid.data.columns)-1:
            jump_before = abs(grid.data.iat[r, c] - grid.data.iat[r, c - 1])
            jump_after = abs(grid.data.iat[r, c] - grid.data.iat[r, c + 1])
            if jump_before >= self.min_jump and jump_after >= self.min_jump:
                rating_multiplier = self.over_incremental_multiplier
                if grid.data.iat[r, c - 1] == grid.data.iat[r, c + 1]:
                    rating_multiplier = rating_multiplier * self.back_again_multiplier
                grid.add_tally(r, c, (jump_before+jump_after)*self.over_incremental_multiplier)