import abjad
import calliope

class Fragment(calliope.Machine):
    """
    Some fragment of machine-based bubbles. Base class for all machines that
    contain child machines.
    """
    meter = None
    defined_length = None # pre-determined length in beats, will pad rests at end if needed
    time_signature = None # TO DO MAYBE consider making time signature a property with a setter
    pickup = None # must be able to be represented as a single note with no dots
    bar_line = None # TO DO: keep?

    # TO DO: consider whether these attributes should only apply to FragmentRow
    pitches_skip_rests = False

    print_kwargs = ("beats",)    # TO CONSIDER... SEPARATE ABOVE EVENT FROM EVENT ITSELF
    
    # TO DO MAYBE, only makes sense as an init_
    _transposition = 0 
    sort_init_attrs = ("rhythm", "transpose", "pitches_skip_rests", "pitches")


    # init_rhythm = ()
    # init_pitches = ()
    # init_bookend_rests = ()

    # TO DO MAYBE: keep transposition away from the class attribute level?
    # (other than a transpose method)

    # TO DO MAYBE: make bookend_rests a property with a setter method
    def _init_set_bookend_rests(self, bookend_rests=()):
        self.add_bookend_rests(*bookend_rests)

    def _init_set_transpose(self, transpose=0):
        self._transposition = transpose

    def _init_set_pitches(self, pitches=()):
        # # TO DO: DEAL WITH TRANSPOSITION ???
        # transposition = ...
        # if transposition:
        #     pitches = [p + transposition for p in pitches]
        self.pitches = pitches

    @property
    def rest(self):
        return all([l.rest for l in self.logical_ties])

    @rest.setter
    def rest(self, is_rest:bool):
        print("WARNING SETTING REST ON FRAGMENT")
        for l in self.logical_ties: # TO DO... what about custom here?
            l.rest = is_rest # NOTE... turning OFF rests could result in odd behavior!

    @property
    def skip(self):
        return all([l.skip for l in self.logical_ties])

    @rest.setter
    def skip(self, is_skip:bool):
        print("WARNING SETTING SKIP ON FRAGMENT")
        for l in self.logical_ties: # TO DO... what about custom here?
            l.skip = is_skip # NOTE... turning OFF rests could result in odd behavior!

    def append_rhythm(self, beats):
        # note, this is overriden on Event so that events will create a rhythm out of 
        # logical ties as opposed to events of events in an infinite loop
        self.append( calliope.Event(beats=beats))

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
        self.set_pitches(values, self.pitches_skip_rests)

    def set_pitches(self, values, skip_rests=False):
        if skip_rests:
            values = list(values)
            for i,e in enumerate(self.events):
                if (e.rest or e.skip) and i <= len(values):
                    values.insert(i, e.pitch)

        my_length = len(self.events)

        for i, v in enumerate(values[:my_length]):
            self.events[i].pitch = v

    @property
    def logical_tie_pitches(self):
        return [l.pitch for l in self.logical_ties]

    @property
    def pitch_set(self):
        my_set = set()
        for p in self.pitches:
            if p.is_chord:
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

    def transpose(self, interval):
        def transpose_thingy(thingy, interval):
            if thingy.pitch.is_chord:
                for i, pitch in thingy.pitch:
                    thingy.pitch[i] = abjad.NamedPitch(thingy.pitch[i]).transpose(interval)
            else:
                thingy.pitch = abjad.NamedPitch(thingy.pitch).transpose(interval)

        for n in self.note_events:
            transpose_thingy(n, interval)

        for l in self.logical_ties.exclude(pitch=None):
            transpose_thingy(l, interval)


    def ticks_before(self, ancestor_branch):
        running_count = 0
        my_first_logical_tie = self.logical_ties[0]
        for l in ancestor_branch.logical_ties:
            if l is my_first_logical_tie:
                return running_count
            running_count += l.ticks
        return running_count

    def beats_before(self, ancestor_branch):
        ticks_before = self.ticks_before(ancestor_branch)
        return ticks_before / calliope.MACHINE_TICKS_PER_BEAT




    # TO DO: ticks_before and ticks_after ever used? KISS?
    # @property
    # def ticks_before(self):
    #     if self.children:
    #         return self.children[0].ticks_before
    #     return 0

    # @property
    # def ticks_after(self):
    #     return self.ticks_before + self.ticks