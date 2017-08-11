import abjad
from calliope import machines

class Transpose(machines.Transform):
    interval = 0 

    def transform_nodes(self, machine):
        for event in machine.events:
            event.transpose(self.interval)

class Displace(Transpose):
    interval = 12
    multiple = 1

    def __init__(self, multiple=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if multiple:
            self.multiple = multiple

    def transform_setup(self, machine):
        self.interval = self.interval * self.multiple

class DisplaceFifths(Displace):
    interval = 7

