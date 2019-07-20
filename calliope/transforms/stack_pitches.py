import abjad
import calliope

# TO DO: FIX DUPE CLASS NAME (with factory)!!!
class StackPitches(calliope.Transform):
    """
    convert individual notes to chords
    """
    intervals = (0,)

    def transform(self, selectable, **kwargs):
        for event in selectable.note_events:
            if isinstance(event.pitch, (list, tuple)):
                event.pitch = [p + ip for p in event.pitch for ip in self.intervals]
            elif event.pitch is not None:
                event.pitch = [ip + event.pitch for ip in self.intervals]

