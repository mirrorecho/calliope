import abjad
import calliope

class TenuStacca(calliope.Transform):
    """
    longer notes are tenuto, shorter staccato
    """
    break_beats=1

    def transform(self, selectable, **kwargs):
        for e in selectable.note_events:
            if e.beats >= self.break_beats:
                e.tag("-")
            else:
                e.tag(".")


