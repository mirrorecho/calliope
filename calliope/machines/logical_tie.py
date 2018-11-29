import calliope

class LogicalTie(calliope.Machine):
    # original_duration = 0 # TO DO: USE THIS?
    is_simultaneous = False
    print_kwargs = ("beats", "pitch", "rest")
    ticks = 0
    pitch = None # if None, defaults to Event's pitch
    rest = False

    # TO DO: used? or KISS?
    is_primary = True # True if this logical tie is a primary one for it's parent event

    can_have_children = True
    must_have_children = False

    select_property = "logical_ties"

    @property
    def signed_ticks(self):
        return self.ticks if not self.rest else 0 - self.ticks

    @property
    def beats(self):
        return super().beats

    @beats.setter
    def beats(self, value):
        if value < 0:
            self.rest = True
        self.ticks = abs(int(value * calliope.MACHINE_TICKS_PER_BEAT))

    @property
    def signed_beats(self):
        return super().beats if not self.rest else 0 - super().beats 

    @property
    def use_ancestor_attachments(self):
        # TO DO: reconsider?
        """
        If a rest(s) precede the first note in this logical tie's event,
        this causes ancestor attachments to always be attached to that first note 
        (as opposed to rest). If the entire event is a rest, then attach to the
        first rest.
        """
        return self.is_first_non_rest or (self.my_index == 0 and self.parent.rest)

    @property
    def is_first_non_rest(self):
        return self is self.parent.first_non_rest

    # TO DO: used? or KISS?
    @property
    def ticks_before(self):
        running_count = 0
        # TO DO: shouldn't go to root for blocks!
        for l in self.root.logical_ties_or_container:
            if l is self:
                return running_count
            running_count += l.ticks
        return running_count

    # TO DO: used? or KISS?
    @property
    def ticks_after(self):
        return self.ticks_before + self.ticks

    def music(self, **kwargs):
        self.warn("Calling music on logical tie not supported. Returning parent event's music instead")
        return self.parent.music()