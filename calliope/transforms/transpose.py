import abjad
import calliope

# TO DO... these transforms are super basic... even worth it?

class Transpose(calliope.Transform):
    interval = 0 

    def transform(self, selectable, **kwargs):
        for event in selectable.non_rest_events:
            event.transpose(self.interval)

class Displace(calliope.Transform):
    interval = 12
    multiple = 1

    def transform(self, selectable, **kwargs):
        for event in selectable.non_rest_events:
            event.transpose(self.interval * self.multiple)

class DisplaceFifths(Displace):
    interval = 7