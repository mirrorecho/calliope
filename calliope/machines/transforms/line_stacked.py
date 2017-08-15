import abjad
import calliope
from calliope import tools, bubbles, machines

class StackedTransform(machines.Transform):
    def transform_nodes(self, machine):
        new_lines = []
        for i in range(len(machine.intervals[0])):
            for line in machine:
                stack_line = line(name=line.name + "_%s" % i )
                for e, event in enumerate(stack_line.events):
                    # TO DO... assumes that there are no chords... also may want
                    # a more generalized transpose on event / logical tie
                    event.transpose(machine.intervals[e % len(machine.intervals)][i])
                new_lines.append(stack_line)
        machine[:] = new_lines



class LineStacked(machines.LineBlock):
    intervals = ( (12,12), (7,12) )
    swaps = (3)
    # line_1 = machines.Line( machines.Event(beats=2, pitch="A4") )
    stack_me = StackedTransform()

    def get_pitch_lines(self):
        return [
            [None if e.pitch is None else abjad.NamedPitch(e.pitch).number for e in line.events ] 
            for line in self
        ]

    def cloud_me(self):
        cloud_pitches = calliope.CloudPitches(
                self.get_pitch_lines()
            )
        cloud_pitches.tally_apps = [
            calliope.TallyCircleOfFifthsRange(over_range_multiplier=-99), 
            # TallyParallelIntervals(interval_ratings=[(0,-20), (7,-11)]), 
            calliope.TallyMelodicIntervals(
                    interval_ratings=[(0, -80), (1,12), (2,22), (3,9), (4,9), (5,6), (6,-6), (7,-4), (10,-8), (11,-20), (12,-4)], 
                    over_incremental_multiplier=(12,-60),
                    up_rating=-12,
                    down_rating=20,
                    ),
            calliope.TallyRepeatedJumps(),
        ]
        # print("TALLLY!!!")
        cloud = cloud_pitches.tally_loop()
        for line, pitch_line in zip( self, cloud.pitch_lines ):
            for i, event in enumerate(line.events):
                event.pitch = pitch_line[i]

    def swap_events(self, swaps=()):
        swaps = swaps or self.swaps
        for s, swap in enumerate(swaps):
            new_vertical = [ self[swap_value].events[s] for swap_value in swap ]
            for i, event in enumerate(new_vertical):
                # TO DO, this is screwy, inelegant, and confusing: rethink...
                event_index = self[i].events[s].my_index
                self[i].events[s].parent[event_index] = event()




# ============================================================

# tools.illustrate_me( bubble=t )
