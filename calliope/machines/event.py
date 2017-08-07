from calliope import machines

class Event(machines.EventMachine):

    pitch = 0 # note, this could be set to a list/tuple to indicate a chord
    original_pitch = 0 # just a way to track what's going on if pitch is transposed
    respell = None # set to "sharps" or "flats" 
    child_types = (machines.LogicalTie,)
    from_line = None # used in FragmentLine for EventData that's copied from another line (tracks where it's copied from)

    def __init__(self, tie_name="tie", beats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if beats:
            # TO DO MAYBE: None indicating rest is a little confusing here (since at the LogicalTie level None for pitch means to use the Event pitch)
            rest = "pitch" in kwargs and kwargs["pitch"] == None

            self[tie_name] = machines.LogicalTie(name=tie_name, beats=beats, rest=rest, *args, **kwargs)

    def append_rhythm(self, beats):
        my_tie = machines.LogicalTie()
        my_tie.beats = beats
        self.append( my_tie )

