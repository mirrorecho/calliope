import calliope

# TO DO... how/whether to use this????
# class LeafData(calliope.TagSet, calliope.Tree):
#     original_duration = 0
#     ticks = 0
#     rest = False


# TO DO MAYBE ... BOTH LogicalTie and Event share some in common
# ... share a mixin?
class LogicalTie(calliope.Machine):
    # original_duration = 0 # TO DO: USE THIS?
    is_simultaneous = False
    print_kwargs = ("beats", "pitch", "rest")
    ticks = 0
    
    _pitch = None # if None, defaults to Event's pitch
    _rest = False
    _skip = False

    is_primary = True # True if this logical tie is a primary one for it's parent event

    can_have_children = True
    must_have_children = False

    select_property = "logical_ties"

    @property
    def rest(self):
        return self._rest

    @rest.setter
    def rest(self, is_rest:bool):
        self._rest = is_rest
        if self._rest:
            self._skip = False
            self._pitch = None

    @property
    def skip(self):
        return self._skip

    @skip.setter
    def skip(self, is_skip:bool):
        self._skip = is_skip
        if self._skip:
            self._rest = False
            self._pitch = "S"

    @property
    def pitch(self):
        if self._rest or self._skip:
            return self._pitch
        elif self._pitch is not None:
            return self._pitch
        elif self.parent is not None:
            return self.parent.pitch

    @pitch.setter
    def pitch(self, pitch):
        calliope.set_machine_pitch(self, pitch)


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
        If rest(s) precede the first note in this logical tie's event,
        this causes ancestor attachments to always be attached to that first note 
        (as opposed to rest). If the entire event is a rest, then attach to the
        first rest.
        """
        return self.is_first_non_rest or (self.my_index == 0 and self.parent.rest)

    @property
    def is_first_non_rest(self):
        return self is self.parent.first_non_rest

    # TO DO: used? or KISS?
    # @property
    # def ticks_before(self):
    #     running_count = 0
    #     # TO DO: shouldn't go to root for blocks!
    #     for l in self.root.logical_ties_or_container:
    #         if l is self:
    #             return running_count
    #         running_count += l.ticks
    #     return running_count

    # TO DO: used? or KISS?
    # @property
    # def ticks_after(self):
    #     return self.ticks_before + self.ticks



    def music(self, **kwargs):
        self.warn("Calling music on logical tie not supported. Returning parent event's music instead")
        return self.parent.music()