from abjad import *
from calliope.work import Arrangement, Part, PianoStaffPart
from calliope.cycles.transform import AddData

# each cycle can just be an arrangement!
class Cycle:
    """
    Represents a single cycle
    """
    data = {} # a dictionary for all kinds of music data
    flags = []
    arrangement = None

    def __init__(self, measures_durations, arrangement_type=Arrangement):
        # measures durations used in many transformations... default to 1 measure of 4/4
        self.measures_durations = measures_durations
        
        self.arrangement = arrangement_type()
        self.fill_skips()

    def arrange_music(self, part_name, music, staff_number=None): #staff_number used for piano/multistaff parts
        part = self.arrangement.parts[part_name]
        if part.is_simultaneous:
            old_music = part[0 if staff_number is None else staff_number]
        else:
            old_music = part
        music_replace = mutate(old_music).replace_measure_contents(music)
        for m_old, m_new in zip(old_music, music_replace):
            m_old = m_new


class CycleLoop:

    def __init__(self, arrangement_type=Arrangement):
        self.cycles = []
        self.transforms = []
        self.arrangement_type = arrangement_type

    def flag_index(self, flag):
        """
        returns the index of the first instance of the specified flag in cycles
        """
        for i, cycle in enumerate(self.cycles):
            if flag in cycle.flags:
                return i

    def add_transform(self, transform):
        self.transforms.append(transform)

    def add_data(self, name, value, **kwargs):
        self.add_transform(AddData(
                        name, 
                        value=value,
                        **kwargs
                        ))

    def add_cycle(self, index=None, add_flags=[], measures_durations=None):
        cycle = Cycle(
                    measures_durations=self.measures_durations if measures_durations is None else measures_durations,
                    arrangement_type=self.arrangement_type)
        if index is None:
            self.cycles.append(cycle)
        else:
            self.cycles.insert(index, cycle)
        cycle.flags = add_flags

    def add_cycle_before(self, flag, add_flags=[]):
        index = self.flag_index(flag)
        if index is not None:
            self.add_cycle(index, add_flags)

    def add_cycle_after(self, flag, add_flags=[]):
        index = self.flag_index(flag)
        if index is not None:
            self.add_cycle(index + 1, add_flags)

    def apply_transforms(self):
        for i, cycle in enumerate(self.cycles):
            for transform in self.transforms:
                previous_cycle = self.cycles[i-1] if i > 0 else None
                if transform.is_active(i, len(self.cycles), cycle.flags):
                    transform.apply(cycle, previous_cycle)

    def make_arrangement(self):
        arrangement = self.cycles[0].arrangement
        for cycle in self.cycles[1:]:
            arrangement.append_arrangement(cycle.arrangement, divider=True)
        return arrangement


