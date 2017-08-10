import abjad
from calliope import structures, machines

class Tagging(machines.Transform):

    def __init__(self, tag_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_dict = tag_dict

    def transform_nodes(self, machine):
        for key, value in self.tag_dict.items():
            if isinstance(value, (tuple, list)):
                machine[key].tag(*value)
            else:
                machine[key].tag(value)
            
class Slur(machines.Transform):
    def __init__(self, slur_start=0, slur_stop=-1, slur_start_string="(", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slur_start = slur_start
        self.slur_stop = slur_stop
        self.slur_start_string = slur_start_string
        self.slur_stop_string = ")" if slur_start_string=="(" else "))"

    def transform_nodes(self, machine):
        machine[self.slur_start].tag(self.slur_start_string)
        machine[self.slur_stop].tag(self.slur_stop_string)


