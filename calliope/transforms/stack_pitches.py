import abjad
import calliope

# TO DO: FIX DUPE CLASS NAME (with factory)!!!
class StackPitches(calliope.Transform):
    """
    convert individual notes to chords
    """
    intervals = ( (0,12), )

    def transform(self, selectable, **kwargs):
        for i, event in enumerate(selectable.note_events):
            my_intervals = self.intervals[i % len(self.intervals)]

            if event.is_chord:
                event.pitch = [p + ip for p in event.pitch for ip in my_intervals]
            else:
                event.pitch = [ip + event.pitch for ip in my_intervals]

