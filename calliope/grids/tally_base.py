class TallyBase:

    # TO DO... some way to window/overlap to tally up longer things effectively?

    row_weights = None # could be used to make the tally count more at given spots
    column_weights = None # could be used to make the tally count more at given spots

    def __init__(self, column_weights=None, row_weights=None,):
        self.column_weights=column_weights
        self.row_weights=row_weights

    def tally_row(self, grid, row_index):
        pass

    def tally_column(self, grid, column_index):
        pass

    def tally_item(self, grid, column_index, row_index):
        pass

    def tally_item_across_rows(self, grid, column_index, row_index, across_row_index):
        pass

    def tally_item_across_columns(self, cloud, column_index, row_index, across_column_index):
        pass