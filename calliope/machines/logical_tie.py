from calliope import machines

class LogicalTie(machines.Machine):
    # original_duration = 0 # TO DO: USE THIS?
    ticks = 0
    pitch = None # if None, defaults to Event's pitch
    rest = False

    def set_data(self, beats=None, pitch=None, rest=False, **kwargs):
        self.beats = beats
        self.pitch = pitch
        self.rest = rest

    def get_signed_ticks_list(self):
        return [self.ticks if not self.rest else 0 - self.ticks]

    @property
    def beats(self):
        return super().beats

    @beats.setter
    def beats(self, value):
        self.ticks = int(value * self.rhythm_default_multiplier)

    @property
    def use_ancestor_attachments(self):
        return self.is_first_non_rest

    @property
    def is_first_non_rest(self):
        return self is self.parent.first_non_rest

    @property
    def ticks_before(self):
        running_count = 0
        for l in self.root.leaves:
            if l is self:
                return running_count
            running_count += l.ticks
    @property
    def ticks_after(self):
        return self.ticks_before + self.ticks