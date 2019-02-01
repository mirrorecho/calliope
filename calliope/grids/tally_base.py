import calliope

# TO DO... some way to window/overlap to tally up longer things effectively?

class TallyBase(calliope.CalliopeBase):
    row_weights = None # could be used to make the tally count more at given spots
    column_weights = None # could be used to make the tally count more at given spots

    def tally_row(self, grid, r):
        pass

    def tally_column(self, grid, c):
        pass

    def tally_item(self, grid, r, c):
        pass

    def tally_item_across_rows(self, grid, r, c, across_r):
        pass

    def tally_item_across_columns(self, cloud, r, c, across_c):
        pass