from abjad import *
from calliope.work import Bubble, Part, PianoStaffPart
from calliope.cycles.transform import AddMaterial, ArrangeMusic, ExecMethod


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

    def add_sub_part(self, **kwargs):
        self.add_transform(ExecMethod("add_sub_part", **kwargs))

    def arrange_music(self, **kwargs):
        self.add_transform(ArrangeMusic(**kwargs))

    def exec_method(self, name, **kwargs):
        self.add_transform(ExecMethod(name, **kwargs))

    def attach(self, **kwargs):
        self.add_transform(ExecMethod("attach", **kwargs))        

    def attach_dynamics(self, **kwargs):
        self.add_transform(ExecMethod("attach_dynamics", **kwargs)) 

    def attach_markup(self, **kwargs):
        self.add_transform(ExecMethod("attach_markup", **kwargs)) 

    def attach_articulations(self, **kwargs):
        self.add_transform(ExecMethod("attach_articulations", **kwargs)) 

    def copy_material(self, material_type, material, copy_to, **kwargs):
        self.add_transform(ExecMethod("copy_material", material_type=material_type, material=material, copy_to=copy_to, **kwargs)) 

    def add_cycle(self, bubble_type=None, index=None, flags=[], **kwargs):
        if bubble_type is None:
            bubble_type = self.bubble_type
        cycle = bubble_type(**kwargs)
        # print(cycle.ly_prepends)
        if index is None:
            self.cycles.append(cycle)
        else:
            self.cycles.insert(index, cycle)
        cycle.flags = flags

    def add_cycle_before(self, before_flag, bubble_type=None, flags=[]):
        index = self.flag_index(before_flag)
        if index is not None:
            self.add_cycle(bubble_type, index, flags)

    def add_cycle_after(self, after_flag, bubble_type=None, flags=[]):
        index = self.flag_index(after_flag)
        if index is not None:
            self.add_cycle(bubble_type, index + 1, flags)

    def make_ly_music(self, ly_folder, section_name, iters, final_bar="||", 
        ly_prepends=None, ly_appends=None, run_iters=None):
        if run_iters is not None:
            iters = run_iters + iters
        self.apply_transforms(iters=iters)
        bubble = self.make_bubble(iters=iters, divider=False)
        if ly_prepends is not None:
            bubble.ly_prepends = ly_prepends
        if ly_appends is not None:
            bubble.ly_appends = ly_appends
        bubble.make_ly_music(ly_folder=ly_folder, section_name=section_name, final_bar=final_bar)

    def show_pdf(self, iters, **kwargs):
        self.apply_transforms(iters=iters)
        bubble = self.make_bubble(iters=iters, divider=True)
        bubble.show_pdf()

    def apply_transforms(self, iters=None, flags=None):
        start_iter = 0
        stop_iter = 50
        for i, cycle in enumerate(self.cycles[start_iter:stop_iter]):
            print("Applying transforms for cycle: #" + str(i))
            # if (iters is None or i in iters) and (flags is None or any([f in cycle.flags for f in flags])):
            #     apply_all=True
            #     print("Applying ALL transforms for cycle: #" + str(i))
            # else:
            #     print("Applying non-critial transforms for cycle: #" + str(i))
            #     apply_all=False
            for transform in self.transforms:
                is_critical = False
                # is_critical = True
                # if isinstance(transform, ArrangeMusic):
                #     is_critical=False
                previous_cycle = self.cycles[i-1] if i > 0 else None
                next_cycle = self.cycles[i+1] if i < len(self.cycles)-1 else None
                # if (apply_all or is_critical):
                if transform.is_active(i, len(self.cycles), 
                            cycle.flags,
                            previous_flags= previous_cycle.flags if previous_cycle is not None else [],
                            next_flags= next_cycle.flags if next_cycle is not None else [],
                            ):
                    transform.apply(cycle, previous_cycle)

    def make_bubble(self, iters=None, flags=None, part_names=None, divider=True):
        bubble = self.bubble_type(measures_durations=[])
        if part_names is not None:
            bubble = bubble.make_fragment_bubble(part_names)
        for i,cycle in enumerate(self.cycles):
            if (iters is None or i in iters) and (flags is None or any([f in cycle.flags for f in flags])):
                print("appending cycle to big bubble: #" + str(i))
                bubble.append_bubble(cycle, divider=divider, fill_self=False)

        return bubble


