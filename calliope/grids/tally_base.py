class TallyBase:

    # TO DO... some way to window/overlap to tally up longer things effectively?

    row_weights = None # could be used to make the tally count more at given spots
    column_weights = None # could be used to make the tally count more at given spots

    def __init__(self, row_weights=None, column_weights=None):
        self.row_weights=row_weights
        self.column_weights=column_weights

    def tally_row(self, grid, row_index):
        pass

    def tally_column(self, grid, column_index):
        pass

    def tally_cell(self, grid, row_index, column_index):
        pass

    def tally_cell_across_rows(self, grid, row_index, column_index, across_row_index):
        pass

    def tally_cell_across_columns(self, cloud, row_index, column_index, across_column_index):
        pass