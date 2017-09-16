import abjad
import calliope

class PitchesThroughGrid(calliope.Transform):
    grid_args = None
    grid_kwargs = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.grid_args = args
        self.grid_kwargs = kwargs

    def transform_nodes(self, machine):
        self.grid = calliope.PitchGrid.from_bubble(machine, *self.grid_args, **self.grid_kwargs)
        for line_index, l in enumerate(machine):
            for note_index, note in enumerate([t for t in l.logical_ties if not t.rest]):
                # NOTE: grid will have numpy.int64 for each pitch, but machine expects int
                # ... change to use duck typing?
                note.pitch = int(self.grid.data.iat[line_index, note_index])


