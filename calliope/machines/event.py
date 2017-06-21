from calliope import machines

class Event(machines.Machine):

    pitch = 0 # note, this could be set to a list/tuple to indicate a chord
    original_pitch = 0 # just a way to track what's going on if pitch is transposed
    respell = None # set to "sharps" or "flats" 
    child_types = (machines.LogicalTie,)
    from_line = None # used in FragmentLine for EventData that's copied from another line (tracks where it's copied from)

    def __init__(self, tie_name="tie0", beats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if beats:
            self[tie_name] = self.branch(name=tie_name, beats=beats, *args, **kwargs)

    # def set_data(self, beats, pitch=0, **kwargs):
    #     self.pitch = pitch
    #     child_tie = self.branch()
    #     child_tie.set_data(beats=beats, **kwargs)

    @property
    def first_non_rest(self):
        for l in self.children:
            if not l.rest:
                return l

    @property
    def last_non_rest(self):
        for l in self.children[::-1]:
            if not l.rest:
                return l

    def remove_bookend_rests(self):
        if self.children:
            if self.children[0].rest:
                self.pop(0)
        if self.children:
            if self.children[-1].rest:
                self.pop(-1)