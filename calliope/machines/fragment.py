class Fragment(Machine):
    """
    Some fragment of machine-based bubbles. Base class for all machines that
    contain child machines.
    """

    print_kwargs = ("beats",)
    bookend_rests = ()
    set_rhythm = None
    set_pitches = None
    pitches_skip_rests = False

    # TO CONSIDER... SEPARATE ABOVE EVENT FROM EVENT ITSELF

    def __init__(self, *args, **kwargs):
        rhythm = kwargs.pop("rhythm", None) or self.set_rhythm
        pitches = kwargs.pop("pitches", None) or self.set_pitches
        pitches_skip_rests = kwargs.pop("pitches_skip_rests", self.pitches_skip_rests)
        super().__init__(*args, **kwargs)

        # TO DO: use? or remove?
        # if self.get_children:
        #     self.extend( self.get_children() )

        if rhythm:
            self.rhythm = rhythm

        if pitches:
            if pitches_skip_rests:
                pitches = list(pitches)
                for i,e in enumerate(self.events):
                    if e.rest and i <= len(pitches):
                        pitches.insert(i, None)
            self.pitches = pitches

        if self.bookend_rests:
            self.add_bookend_rests(*self.bookend_rests)

    def remove_empty(self):
        for child in self:
            if child.ticks == 0:
                self.remove(child)

    @property
    def ticks(self):
        return sum([l.ticks for l in self.logical_ties_or_container])

    @property
    def rest(self):
        return all([l.rest for l in self.logical_ties_or_container])

    @rest.setter
    def rest(self, is_rest):
        for l in self.logical_ties: # TO DO... what about custom here?
            l.rest = is_rest # NOTE... turning OFF rests could result in odd behavior!

    # TO DO: ticks_before and ticks_after ever used? KISS?
    @property
    def ticks_before(self):
        if self.children:
            return self.children[0].ticks_before
        return 0

    @property
    def ticks_after(self):
        return self.ticks_before + self.ticks

    @property
    def rhythm(self):
        return [l.signed_beats for l in self.logical_ties]

    def append_rhythm(self, beats):
        # note, this is overriden on Event so that events will create a rhythm out of 
        # logical ties as opposed to events of events in an infinite loop
        self.append( calliope.Event(rhythm=(beats,) ))

    @rhythm.setter
    def rhythm(self, values):
        my_length = len(self.logical_ties)
        for i, v in enumerate(values):
            if i < my_length:
                self.logical_ties[i].beats = v
            else:
                self.append_rhythm(v)

    @property
    def pitches(self):
        return [l.pitch for l in self.events]

    @property
    def logical_tie_pitches(self):
        return [l.pitch for l in self.logical_ties]

    @pitches.setter
    def pitches(self, values):
        my_length = len(self.events)
        for i, v in enumerate(values[:my_length]):
            self.events[i].pitch = v
            self.events[i].rest = v is None

    @property
    def first_non_rest(self):
        for l in self.logical_ties:
            if not l.rest:
                return l

    @property
    def last_non_rest(self):
        for l in reversed(self.logical_ties):
            if not l.rest:
                return l

    def get_signed_ticks_list(self):
        # TO DO.. there's probably a more elegant one-liner for this!
        return_list = []
        for l in self.logical_ties_or_container:
            return_list.extend(l.get_signed_ticks_list())
        
        if self.defined_length:
            ticks_end = self.ticks
            defined_length_ticks = self.defined_length * self.rhythm_default_multiplier
            if defined_length_ticks > ticks_end:
                return_list.append(int(ticks_end - defined_length_ticks))

        return return_list


    def transpose(self, interval):
        for thing in self.by_type(calliope.Event, calliope.LogicalTie):
            # TO DO... handle tuples
            if thing.pitch is not None:
                if isinstance( thing.pitch, (list, tuple) ):
                    for i, pitch in thing.pitch:
                        thing.pitch[i] = abjad.NamedPitch(thing.pitch[i]).transpose(interval)
                else:
                    thing.pitch = abjad.NamedPitch(thing.pitch).transpose(interval)

    def add_bookend_rests(self, beats_before=0, beats_after=0):
        if beats_before > 0:
            first_event = self.logical_ties[0].parent
            first_event.insert(0, calliope.LogicalTie(rest=True, beats=beats_before))
        if beats_after > 0:
            last_event = self.logical_ties[-1].parent
            last_event.append(calliope.LogicalTie(rest=True, beats=beats_after))

    # TO DO: consider making this cyclic???
    def remove_bookend_rests(self):
        if self.logical_ties:
            if self.logical_ties[0].rest:
                self.logical_ties[0].parent.pop(0)
        if self.logical_ties:
            if self.logical_ties[-1].rest:
                self.logical_ties[-1].parent.pop(-1)

    # TO DO... add slur
    # def slur()