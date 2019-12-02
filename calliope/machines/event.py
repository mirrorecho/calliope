import abjad
import calliope

class Event(calliope.PitchDataMixin, calliope.FragmentRow):
    child_types = (calliope.LogicalTie,)
    select_property = "events"
    print_kwargs = ("beats", "pitch")

    init_beats = 1
    tie_name = None

    sort_init_attrs = ("beats", "rhythm", "transpose", "pitches_skip_rests", "pitch", "pitches", "rest", "skip")

    @property
    def pitch_class(self):
        if self.pitch is None:
            return None
        elif self.is_chord:
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
    def note_pitches(self):
        return [self.pitch] if not self.rest else []

    @property
    def first_primary_tie(self):
        my_tie = next((x for x in self.logical_ties if x.is_primary==True), None)
        
        if my_tie is None:
            my_tie = calliope.LogicalTie(
                name=self.tie_name, 
                is_primary=True,
                )
            self.append(my_tie)
        
        return my_tie

    @property
    # TO DO... needed?
    def signed_beats(self):
        return super().beats if not self.rest else 0 - super().beats 

    @property
    def beats(self):
        return super().beats

    @beats.setter
    def beats(self, value):
        self.first_primary_tie.ticks = abs(int(value * calliope.MACHINE_TICKS_PER_BEAT))
        if value < 0:
            self.rest = True
        elif self.pitch_undefined:
            self.pitch = 0

    def append_rhythm(self, beats):
        # TO DO: needed??
        my_tie = calliope.LogicalTie()

        my_tie.beats = beats
        self.append( my_tie )

    def event_at_beat(self, beats):
        if self.beats > beats:
            return self

