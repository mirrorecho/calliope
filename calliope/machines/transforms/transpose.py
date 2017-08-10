import abjad
from calliope import machines

class Transpose(machines.Transform):
    interval = 0 

    def transform_nodes(self, machine):
        for thing in machine.by_type(machines.Event, machines.LogicalTie):
            # TO DO... handle tuples
            if thing.pitch is not None:
                thing.pitch = abjad.NamedPitch(thing.pitch).transpose(self.interval)

class Displace(machines.Transform):
    interval = 12
    multiple = 1

    def transform_setup(self, machine):
        self.interval = self.interval * self.multiple