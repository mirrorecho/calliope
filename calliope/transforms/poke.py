import abjad
import calliope

# TO DO: this would be cleaner with abstract selections
class Poke(calliope.Transform):
    """
    keeps events in the selection, makes everything else rests
    """
    selection = None

    def transform(self, selectable, **kwargs):

        my_events = list(self.selection.note_events)

        for e in selectable.note_events:
            if not e in my_events:
                e.rest = True


