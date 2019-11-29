import abjad
import calliope

class CropChords(calliope.Transform):
    """
    includes only certain items in chords
    """
    indices = (0,)
    above = (None,)

    def transform(self, selectable, **kwargs):
        cyclic_indices = abjad.CyclicTuple(self.indices)
        cyclic_above = abjad.CyclicTuple(self.above)

        for i, e in enumerate(selectable.note_events):
            index = cyclic_indices[i]
            above = cyclic_above[i]
            if e.is_chord:
                if above is not None:
                    e.pitch = sorted(e.pitch)[index:above]
                else:
                    e.pitch = sorted(e.pitch)[index]
                    



