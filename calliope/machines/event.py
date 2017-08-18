import abjad
import calliope

class Event(calliope.EventMachine):

    pitch = 0 # note, this could be set to a list/tuple to indicate a chord
    original_pitch = 0 # just a way to track what's going on if pitch is transposed
    child_types = (calliope.LogicalTie,)
    from_line = None # used in FragmentLine for EventData that's copied from another line (tracks where it's copied from)
    set_beats = None

    def __init__(self, tie_name="tie", beats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        beats = beats or self.set_beats
        if beats:
            # TO DO MAYBE: None indicating rest is a little confusing here (since at the LogicalTie level None for pitch means to use the Event pitch)
            self.pitch = kwargs.get("pitch", None) or self.pitch
            rest = self.pitch is None

            self[tie_name] = calliope.LogicalTie(name=tie_name, beats=beats, rest=rest, *args, **kwargs)

    def append_rhythm(self, beats):
        my_tie = calliope.LogicalTie()

        my_tie.beats = beats
        self.append( my_tie )

class RestEvent(Event):
    def __init__(self, beats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["rest"] = calliope.LogicalTie(name="rest", beats=beats, pitch=None, rest=True, *args, **kwargs)
