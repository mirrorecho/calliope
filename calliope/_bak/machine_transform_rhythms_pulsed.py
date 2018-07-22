
from calliope import structures, machines

class RhythmsPulsed:
    """
    Simple mixin to pulse rhythmic duration values for any segment
    """

    rhythm_pulses = None # should be set to an indexed data object that defines multiplier for eacch segment index

    def __init__(self, **kwargs):
        self.rhythm_pulses = self.rhythm_pulses or tools.IndexedData()
        super().__init__(**kwargs)


    def set_logical_tie(self, logical_tie, **kwargs):
        super().set_logical_tie(logical_tie, **kwargs)
        if not logical_tie.rest:
            pulse_duration = logical_tie.parent.parent.rhythm_pulse_duration
            if pulse_duration:
                pulse_ticks = int(pulse_duration * self.rhythm_default_multiplier)
                if self.verify(logical_tie.ticks >= pulse_ticks, 
                            "can't pulse because pulse duration >= logical tie duration", logical_tie):
                    if self.verify(logical_tie.ticks % pulse_ticks == 0, 
                            "can't pulse because logical tie duration can't be evenly divided by pulse duration", logical_tie):
                        for i in range( int(logical_tie.ticks / pulse_ticks) - 1):
                            logical_tie.parent.insert(logical_tie.my_index, calliope.LogicalTieData(ticks=pulse_ticks) )
                        logical_tie.ticks = pulse_ticks
        # logical_tie.ticks = int(logical_tie.ticks * self.rhythm_multipliers[segment_index])

    def set_segment(self, segment, **kwargs):
        super().set_segment(segment, **kwargs)
        setattr(segment, "rhythm_pulse_duration", self.rhythm_pulses[segment.my_index])