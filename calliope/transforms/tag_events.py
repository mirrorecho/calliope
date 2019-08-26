import abjad
import calliope

class CropChords(calliope.Transform):
    """
    includes only certain items in chords
    """
    below = None
    above = None
    index = None

    def transform(self, selectable, **kwargs):
        for e in selectable.note_events:
            if isinstance(e.pitch, (list, tuple)):
                if self.index is not None:
                    e.pitch = sorted(e.pitch)[self.index]
                else:
                    e.pitch = sorted(e.pitch)[self.below:self.above]



