import calliope

# TO DO... some way to window/overlap to tally up longer things effectively?

class TallyBase(calliope.CalliopeBaseMixin):
    row_weights = None # could be used to make the tally count more at given spots
    column_weights = None # could be used to make the tally count more at given spots

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