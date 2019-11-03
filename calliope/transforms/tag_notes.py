import abjad
import calliope

class TagNotes(calliope.Transform):
    """
    includes only certain items in chords
    """
    tags = ()

    def transform(self, selectable, **kwargs):
        selectable.note_events.tag(*self.tags)



