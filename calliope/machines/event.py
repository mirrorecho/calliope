import abjad
import calliope

class Event(calliope.FragmentRow):
    child_types = (calliope.LogicalTie,)
    select_property = "events"
    print_kwargs = ("beats", "pitch")

    # TO DO MAYBE: force numeric value??
    pitch = 0 # this could be set to a list/tuple to indicate a chord
    init_beats = 1
    tie_name = None

    @property
    def pitch_class(self):
        if self.pitch is None:
            return None
        elif isinstance(self.pitch, (list, tuple)):
            return [p % 12 for p in self.pitch]
        else:
            return self.pitch % 12

    @property
    def pitches(self):
        return [self.pitch]

    @pitches.setter
    def pitches(self, values):
        if values:
            self.pitch = values[0]

    @property
    def first_primary_tie(self):
        my_tie = next((x for x in self.logical_ties if x.is_primary==True), None)
        if my_tie is None:
            my_tie = calliope.LogicalTie(name=self.tie_name, is_primary=True)
            self.append(my_tie)
        return my_tie

    @property
    def beats(self):
        return super().beats

    @property
    # TO DO... needed?
    def signed_beats(self):
        return super().beats if not self.rest else 0 - super().beats 

    @beats.setter
    def beats(self, value):
        self.first_primary_tie.ticks = abs(int(value * calliope.MACHINE_TICKS_PER_BEAT))
        if value < 0:
            self.rest = True

    @property
    def rest(self):
        return super().rest

    @rest.setter
    def rest(self, is_rest):
        if is_rest:
            self.pitch = None
        for l in self.logical_ties: # TO DO... what about custom here?
            l.rest = is_rest # NOTE... turning OFF rests could result in odd behavior!

    def append_rhythm(self, beats):
        # TO DO: needed??
        my_tie = calliope.LogicalTie()

        my_tie.beats = beats
        self.append( my_tie )

