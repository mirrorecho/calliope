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


class Displace(calliope.Transform):
    interval = 12
    multiple = 1

    def transform(self, selectable, **kwargs):
        for event in selectable.note_events:
            event.transpose(self.interval * self.multiple)

class DisplaceFifths(Displace):
    interval = 7