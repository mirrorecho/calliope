
from calliope import bubbles, structures, machines

class PitchDisplacementData(tools.IndexedData):
    default = lambda self=None : set(  )
    cyclic=False
    items_type = set

    # TO DO... add set operators (set operation to be applied to each item)
    # TO DO... consider implementing or more general base case of IndexedData where each item is a set...

    def __setitem__(self, key, value):
        if isinstance(value, set):
            super().__setitem__(key, value)
        elif isinstance(value, tuple) or isinstance(value, list):
            super().__setitem__(key, set(value)) # TO DO.. this line should be enough.... 
        else:
            raise TypeError("PitchDisplacementData item value must be a set, or a list or tuple (to be converted to a set)")

    def update_item(self, index, intervals):
        if index in self.keylist():
            self[index] |= set(intervals)
        else:
            self[index] = set(intervals)       

    def update(self, from_dict):
        if isinstance(from_dict, PitchDisplacementData):
            for i, intervals in from_dict.non_default_items():
                self.update_item(i, intervals)
            if self.limit <= max(from_dict.data):
                self.limit = max(from_dict.data) + 1
        else:
            super().update(from_dict)

    def remove_from_item(self, index, intervals):
         if index in self.keylist():
            self[index] -= set(intervals)

    def get_sum(self, index, only_intervals=None):
        if only_intervals:
            return sum( self[index] & set(only_intervals) )
        else:
            return sum( self[index] )

    def get_cumulative(self, index=None, only_intervals=None): # index can be None to return the entire cumulative displacement sum
        my_sum = 0
        for i in self.keylist():
            if index and i > index:
                break
            my_sum += self.get_sum(i, only_intervals)
        return my_sum

    def cycle_interval(self, start_index=0, interval=0, cycle=(), times=0):
        # TO DO... thought... maybe cycle would be better defined as an Indexed Data object (as opposed to tuple?)
        for i in range(len(cycle) * times):
            interval_multiplier = cycle[i % len(cycle)]
            if interval_multiplier != 0:
                self.update_item(start_index+i, (interval*interval_multiplier,))


class IntervalDisplacement(PitchDisplacementData):
    displacement_interval = 0

    def __init__(self, initialize_from=None, up=(), down=(), flat=(), **kwargs):
        super().__init__(**kwargs)
        self.up(*up)
        self.down(*down)
        self.flat(*flat)

    def cycle_me(self, start_index=0, **kwargs):
        self.cycle_interval(start_index=start_index, interval=self.displacement_interval, **kwargs)

    def up(self, *indices):
        if indices:
            self.fillme(indices, (self.displacement_interval,))

    def down(self, *indices):
        if indices:
            self.fillme(indices, (self.displacement_interval * -1,))

    # TO DO.. this naming is confusing (i.e. confused with sharp/flat vs not up/down)
    def flat(self, *indices):
        if indices:
            for i in indices:
                self.remove_from_item(i, (self.displacement_interval,self.displacement_interval * -1))

class FifthDisplacement(IntervalDisplacement):
    displacement_interval = 7

class OctaveDisplacement(IntervalDisplacement):
    displacement_interval = 12

class PitchesDisplaced(object):
    """
    Mixin for displacing pitches in a segmented line.
    """
    pitch_displacement = None

    def get_pitch_displacement(self, **kwargs):
        """
        Could be overriden to fancify modify pitch displacment data on the fly.
        """
        if self.pitch_displacement:
            return self.pitch_displacement
        return machines.PitchDisplacementData(**kwargs)

    def set_event(self, event, **kwargs):
        super().set_event(event, **kwargs)
        pitch_displacement = self.get_pitch_displacement(**kwargs)
        event.pitch = event.original_pitch + pitch_d