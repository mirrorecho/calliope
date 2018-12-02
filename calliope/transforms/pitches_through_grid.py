import abjad
import calliope

class PitchesThroughGrid(calliope.Transform):
    tally_apps = ()
    version = None
    pitch_ranges = None

    def transform_nodes(self, machine):
        version = self.version or getattr(machine, "grid_version", 1)
        setattr(machine, "pitch_grid", calliope.PitchGrid.from_bubble(
                    machine, 
                    *self.tally_apps, 
                    version = version,
                    pitch_ranges = self.pitch_ranges,
                    )
                )
        for line_index, l in enumerate(machine):
            for event_index, event in enumerate([e for e in l.note_events]):
                # NOTE: grid will have numpy.int64 for each pitch, but machine expects int
                # ... change to use duck typing?
                event.pitch = int(machine.pitch_grid.data.iat[line_index, event_index])


