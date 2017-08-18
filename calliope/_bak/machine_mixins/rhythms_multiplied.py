import abjad
from calliope import bubbles, tools


class RhythmsMultiplied:
    """
    Simple mixin to multiply relative rhythmic duration values for any segment
    """

    rhythm_multipliers = None # should be set to an indexed data object that defines multiplier for eacch segment index

    @classmethod
    def make_multipliers(cls, multipliers=None, default=1, cyclic=False, **kwargs):
        return tools.IndexedData(multipliers, default=default, cyclic=cyclic, **kwargs)

    def __init__(self, **kwargs):
        self.rhythm_multipliers = self.rhythm_multipliers or RhythmsMultiplied.make_multipliers() # defaults multipliers to 1
        super().__init__(**kwargs)


    def set_logical_tie(self, logical_tie, **kwargs):
        super().set_logical_tie(logical_tie, **kwargs)
        segment_index = logical_tie.parent.parent.my_index
        logical_tie.ticks = int(logical_tie.ticks * self.rhythm_multipliers[segment_index])

    def set_segment(self, segment, **kwargs):
        super().set_segment(segment, **kwargs)
        segment.rhythm_segment_multiplier = self.rhythm_multipliers[segment.my_index]