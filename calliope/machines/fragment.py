import abjad
import calliope

class Fragment(calliope.Machine):
    """
    Some fragment of machine-based bubbles. Base class for all machines that
    contain child machines.
    """
    meter = None
    defined_length = None # pre-determined length in beats, will pad rests at end if needed
    bookend_rests = ()
    time_signature = None
    pickup = None # must be able to be represented as a single note with no dots
    bar_line = None # TO DO: keep?

    # TO DO: consider whether these attributes should only apply to FragmentRow
    pitches_skip_rests = False

    print_kwargs = ("beats",)    # TO CONSIDER... SEPARATE ABOVE EVENT FROM EVENT ITSELF
    transpose = 0

    
    # dub_rhythm = ()
    # dub_pitches = ()


    def __init__(self, *args, **kwargs):
        pitches_skip_rests = kwargs.pop("pitches_skip_rests", self.pitches_skip_rests)
        super().__init__(*args, **kwargs)

        if self.transpose:
            pitches = [p + self.transpose for p in pitches]

        if pitches:
            if pitches_skip_rests:
                pitches = list(pitches)
                for i,e in enumerate(self.events):
                    if e.rest and i <= len(pitches):
                        pitches.insert(i, None)
            self.pitches = pitches

        # TO DO, make this 
        if self.bookend_rests:
            self.add_bookend_rests(*self.bookend_rests)

    @property
    def rest(self):
        return all([l.rest for l in self.logical_ties])

    @rest.setter
    def rest(self, is_rest):
        for l in self.logical_ties: # TO DO... what about custom here?
            l.rest = is_rest # NOTE... turning OFF rests could result in odd behavior!

    def append_rhythm(self, beats):
        # note, this is overriden on Event so that events will create a rhythm out of 
        # logical ties as opposed to events of events in an infinite loop
        self.append( calliope.Event(rhythm=(beats,) ))

    @property
    def rhythm(self):
        return [l.signed_beats for l in self.logical_ties]

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

    @pitches.setter
    def pitches(self, values):
        my_length = len(self.events)
        for i, v in enumerate(values[:my_length]):
            self.events[i].pitch = v
            self.events[i].rest = v is None

    @property
    def logical_tie_pitches(self):
        return [l.pitch for l in self.logical_ties]

    @property
    def pitch_set(self):
        my_set = set()
        for p in self.pitches:
            if isinstance(p, (list, tuple)):
                my_set = my_set | set(p)
            else:
                my_set.add(p)
        return my_set

    @property
    def pitch_class_set(self):
        return set([p % 12 for p in self.pitch_set])

    @property
    def first_non_rest(self):
        for l in self.logical_ties:
            if not l.rest:
                return l

    # TO DO: used? or KISS?
    @property
    def last_non_rest(self):
        for l in reversed(self.logical_ties):
            if not l.rest:
                return l

    # TO DO: test... still works? used?
    # def transpose(self, interval):
    #     for thing in self.by_type(calliope.Event, calliope.LogicalTie):
    #         # TO DO... handle tuples
    #         if thing.pitch is not None:
    #             if isinstance( thing.pitch, (list, tuple) ):
    #                 for i, pitch in thing.pitch:
    #                     thing.pitch[i] = abjad.NamedPitch(thing.pitch[i]).transpose(interval)
    #             else:
    #                 thing.pitch = abjad.NamedPitch(thing.pitch).transpose(interval)


    # TO DO: ticks_before and ticks_after ever used? KISS?
    # @property
    # def ticks_before(self):
    #     if self.children:
    #         return self.children[0].ticks_before
    #     return 0

    # @property
    # def ticks_after(self):
    #     return self.ticks_before + self.ticks