import abjad
import calliope

class PitchDataMixin(object):

    _pitch_data = None
    # int : a note's pitch
    # tuple (of ints) : chord
    # "S" : skip
    # "R" : rest

    # None : undefined (if parent has pitch data, 
    #        then will use that, otherwise, render as rest)

    @property
    def pitch(self):
        if self._pitch_data is None and self.parent:
            return getattr(self.parent, "pitch", None)
        else:
            return self._pitch_data


    @pitch.setter
    def pitch(self, pitch_data):
        if pitch_data in ("S","R", None):
            self._pitch_data = pitch_data
        else:
            self._pitch_data = calliope.get_pitch_number(pitch_data)

    @property
    def pitch_numbers(self):
        """
        convenience property returns all pitches as list 
        excludes rests and skips
        always returns sorted list (whether chord or not)
        """
        my_pitches = self.pitch if self.is_chord else [self.pitch]
        my_pitches = [p for p in my_pitches if isinstance(p, int)]
        return sorted(my_pitches)

    @property
    def skip(self):
        return self.pitch == "S"

    @skip.setter
    def skip(self, is_skip:bool):
        if is_skip:
            self.pitch = "S"

    @property
    def rest(self):
        return self.pitch == "R"

    @rest.setter
    def rest(self, is_rest:bool):
        if is_rest:
            self.pitch = "R"

    @property
    def render_as_rest(self):
        return self.pitch in ("R", None)

    @property
    def skip_or_rest(self):
        return self.pitch in ("R", "S")

    @property
    def rest_can_combine(self):
        return self.render_as_rest and len(self.get_all_tags())==0

    @property
    def pitch_undefined(self):
        return self._pitch_data is None

    @property
    def is_chord(self):
        return isinstance(self.pitch, tuple)