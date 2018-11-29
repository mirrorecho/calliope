import abjad
import calliope

class Event(calliope.FragmentLine):
    child_types = (calliope.LogicalTie,)
    select_property = "events"
    print_kwargs = ("beats", "pitch")

    pitch = 0 # this could be set to a list/tuple to indicate a chord
    set_beats = None

    # TO DO: remove tie_name / beats ?
    def __init__(self, *args, **kwargs):
        beats = kwargs.pop("beats", None) or self.set_beats
        tie_name = kwargs.pop("tie_name", "tie") or self.tie_name
        super().__init__(*args, **kwargs)
        if beats:
            # TO DO MAYBE: None indicating rest is a little confusing here (since at the LogicalTie level None for pitch means to use the Event pitch)
            self.pitch = kwargs.get("pitch", None) or self.pitch
            rest = self.pitch is None

            self[tie_name] = calliope.LogicalTie(name=tie_name, beats=beats, rest=rest, *args, **kwargs)

    @property
    def first_primary_tie(self):
        return next(x for x in self if x.is_primary)

    @property
    def beats(self):
        return super().beats

    @property
    # TO DO... needed?
    def signed_beats(self):
        return super().beats if not self.rest else 0 - super().beats 

    @beats.setter
    def beats(self, value):
        if value < 0:
            self.rest = True
        self.first_primary_tie.ticks = abs(int(value * calliope.MACHINE_TICKS_PER_BEAT))

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
        my_tie = calliope.LogicalTie()

        my_tie.beats = beats
        self.append( my_tie )

