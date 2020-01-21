import abjad
import calliope

class CropChords(calliope.Transform):
    """
    includes only certain items in chords
    """
    indices = (0,)
    above = (None,)
    below = (None,)

    def transform(self, selectable, **kwargs):
        cyclic_indices = abjad.CyclicTuple(self.indices)
        cyclic_above = abjad.CyclicTuple(self.above)
        cyclic_below = abjad.CyclicTuple(self.below)

        for i, e in enumerate(selectable.note_events):
            index = cyclic_indices[i]
            above = cyclic_above[i] 
            below = cyclic_below[i] 

            if e.is_chord:
                if above is not None or below is not None:
                    my_pitch = sorted(e.pitch)[above:below]
                    if len(my_pitch) == 1:
                        my_pitch = my_pitch[0]
                elif isinstance(index, (list, tuple)):
                    my_pitch = [p for i,p in enumerate(sorted(e.pitch)) if i in index]
                else:
                    my_pitch = sorted(e.pitch)[index]
                e.pitch = my_pitch
                    



