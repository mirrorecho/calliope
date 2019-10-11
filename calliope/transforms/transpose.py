import math
import abjad
import calliope

# TO DO... these transforms are super basic... even worth it?
class Transpose(calliope.Transform):
    interval = 0 

    def transform(self, selectable, **kwargs):
        for event in selectable.note_events:
            my_pitch = event.pitch
            if isinstance(my_pitch, (list, tuple)):
                event.pitch = [p + self.interval for p in my_pitch]
            else:
                event.pitch += self.interval


# TO DO... this needs to be updated per the above
class Displace(calliope.Transform):
    interval = 12
    multiple = 1

    def transform(self, selectable, **kwargs):
        for event in selectable.note_events:
            event.transpose(self.interval * self.multiple)

class DisplaceFifths(Displace):
    interval = 7


class TransposeWithinScale(calliope.Transform):
    """
    Transposes by steps within a 'calliope.Scale'. Could be within 
    the same scale, or a new scale.
    """

    scale = None
    new_scale = None

    scale_pitches = None
    new_scale_pitches = None
    
    steps = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.scale:
            self.scale = calliope.Scale(self.scale_pitches)

        if not self.new_scale:
            if self.new_scale_pitches:
                self.new_scale = calliope.Scale(self.new_scale_pitches)
            else:
                self.new_scale = self.scale

    def transform(self, selectable, **kwargs):
        for event in selectable.note_events:
            my_pitch = event.pitch

            if isinstance(my_pitch, (list, tuple)):
                event.pitch = [self.scale.pitch_change_scale(
                    p,
                    self.new_scale,
                    self.steps,
                    ) for p in my_pitch]
            else:
                event.pitch = self.scale.pitch_change_scale(
                    my_pitch,
                    self.new_scale,
                    self.steps
                    )


