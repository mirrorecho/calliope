from abjad import *
from calliope.work import Bubble, Part, PianoStaffPart
from calliope.cycles.transform import AddMaterial, ArrangeMusic


class CycleLoop:

    def __init__(self, bubble_type=Bubble):
        self.cycles = []
        self.transforms = []
        self.bubble_type = bubble_type

    def flag_index(self, flag):
        """
        returns the index of the first instance of the specified flag in cycles
        """
        for i, cycle in enumerate(self.cycles):
            if flag in cycle.flags:
                return i

    def add_transform(self, transform):
        self.transforms.append(transform)

    def add_material(self, name, value, **kwargs):
        self.add_transform(AddMaterial(
                        name, 
                        value=value,
                        **kwargs
                        ))

    def add_pitch_material(self, name, value, **kwargs):
        self.add_material(name, value, material_type="pitch", **kwargs) 

    def add_rhythm_material(self, name, value, **kwargs):
        self.add_material(name, value, material_type="rhythm", **kwargs) 

    def arrange_music(self, **kwargs):
        self.add_transform(ArrangeMusic(**kwargs))

    def exec_method(self, name, **kwargs):
        self.add_transform(ExecMethod(name, **kwargs))

    def add_cycle(self, bubble_type=None, index=None, add_flags=[], **kwargs):
        if bubble_type is None:
            bubble_type = self.bubble_type
        cycle = bubble_type(**kwargs)
        if index is None:
            self.cycles.append(cycle)
        else:
            self.cycles.insert(index, cycle)
        cycle.flags = add_flags

    def add_cycle_before(self, flag, bubble_type=None, add_flags=[]):
        index = self.flag_index(flag)
        if index is not None:
            self.add_cycle(bubble_type, index, add_flags)

    def add_cycle_after(self, flag, bubble_type=None, add_flags=[]):
        index = self.flag_index(flag)
        if index is not None:
            self.add_cycle(bubble_type, index + 1, add_flags)

    def apply_transforms(self):
        for i, cycle in enumerate(self.cycles):
            for transform in self.transforms:
                previous_cycle = self.cycles[i-1] if i > 0 else None
                if transform.is_active(i, len(self.cycles), cycle.flags):
                    transform.apply(cycle, previous_cycle)

    def make_bubble(self):
        bubble = self.bubble_type(measures_durations=[])
        for cycle in self.cycles[:]:
            bubble.append_bubble(cycle, divider=True)
        return bubble


