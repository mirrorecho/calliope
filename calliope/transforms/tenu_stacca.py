import abjad
import calliope

class TenuStacca(calliope.Transform):
    """
    includes only certain items in chords
    """
    break_beats=1

    def transform(self, selectable, **kwargs):
        for e in selectable.note_events:
            if e.beats >= self.break_beats:
                self.tag("-")
            else:
                self.tag(".")


