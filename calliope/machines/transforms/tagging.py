import abjad
import calliope

class Tagging(calliope.Transform):

    def __init__(self, tag_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_dict = tag_dict

    def transform_nodes(self, machine):
        for key, value in self.tag_dict.items():
            if isinstance(key, (tuple, list)):
                key_item = machine[key[0]]
                for k in key[1:]:
                    key_item = key_item[k]
            else:
                key_item = machine[key]

            if isinstance(value, (tuple, list)):
                key_item.tag(*value)
            else:
                key_item.tag(value)
            
class Slur(calliope.Transform):
    def __init__(self, slur_start=0, slur_stop=-1, slur_start_string="(", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slur_start = slur_start
        self.slur_stop = slur_stop
        self.slur_start_string = slur_start_string
        self.slur_stop_string = ")" if slur_start_string=="(" else "))"

    def transform_nodes(self, machine):
        machine[self.slur_start].tag(self.slur_start_string)
        machine[self.slur_stop].tag(self.slur_stop_string)


