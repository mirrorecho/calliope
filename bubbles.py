from collections import Mapping
from copy import deepcopy
from collections import OrderedDict
import json

from abjad import *



class Material(dict):
    def __init__(self):
        self.loaded = set()

    @staticmethod
    def update_recursive(to_dict, from_dict):
        for key, value in from_dict.items():
            if isinstance(value, dict):
                to_dict[key] = Material.update_recursive(value, to_dict.get(key, {}))
            else:
                to_dict[key] = deepcopy(from_dict[key])
        return to_dict


    def update(self, from_dict):
        Material.update_recursive(self, from_dict)


    def load(self, name, key_name=None, path="./data", *args, **kwargs):
        
        key_name = key_name or name

        file_path = path + "/" + name + ".json"
        if not name in self or not isinstance(self[name], dict):
            self[name] = Material()
        
        with open(file_path) as data_file:    
            data = json.load(data_file)
            self[name].update(data)

        self.loaded.add(name)

    def use(self, name, *args, **kwargs):
        """
        similar to load, but only loads if not already loaded
        """
        if name not in self.loaded:
            self.load(name, *args, **kwargs)

    def clear(self):
        super().clear()
        self.loaded.clear


GLOBAL_MATERIAL = Material()

class Line():
    def __init__(self, name, initial_music=None, *args, **kwargs):
        self.initial_music = initial_music
        self.name=name

    def generate(self, *args, **kwargs):
        line = Context(name=self.name, *args, **kwargs)
        line.extend(self.initial_music)
        return line


class Bubble():

    def __init__(self, 
            name="a-bubble", 
            *args, **kwargs
            ):
        super().__init__(*args, **kwargs)
        self.name=name
        self.is_simultaneous = True

        self.lines = OrderedDict() # necessary?
        self.material = Material()

        # a little hacky... but works well... this calls the music method on every base class
        for c in reversed( type(self).mro()[:-2] ):
            # print(c)
            if hasattr(c, "music"):
                c.music(self, *args, **kwargs)
                pass

    @classmethod
    def sequence(cls, bubbles=[], name="a-sequence"):
        print(cls)
        mybubble = cls(name=name)
        # TO DO... FIX LENGTHS
        for b in bubbles:
            mybubble.use_lines(b.lines)
        for b in bubbles:
            for n, l in b.lines.items():
                mybubble.lines[n].extend(l)
        return mybubble

    def rename_line(self, old_name, new_name):
        self.lines[new_name] = self.lines.pop(old_name)
        self.lines[new_name].name = new_name

    def use_material(self, name, *args, **kwargs):
        GLOBAL_MATERIAL.use(name, *args, **kwargs)
        self.material.update(GLOBAL_MATERIAL[name])
        self.material.loaded.add(name)


    def music(self, *args, **kwargs):
        """
        default hook...
        """
        pass

    #CONTINUE TO USE THESE? OR SIMPLIFY AS SIMPLY A FUNCTION THAT RETURNS A NEW/EXISTING VOICE?
    def use_lines(self, names, *args, **kwargs):
        for l in names:
            self.use_line(l)

    def use_line(self, name, *args, **kwargs):
        if name not in self.lines:
            line = Context(name=name, *args, **kwargs)
            self.append(line)
            self.lines[name] = line


    # TO DO... make this better
    def score(self):
        """
        a quick way to get a score with auto-generated staves for showing a bubble 
        """
        score = Score()
        for n,v in self.lines.items():
            staff = Staff(name=n+"-staff")
            # staff_voice = Context(name=v, context_name="Voice")
            staff.append(v)
            instrument = instrumenttools.Instrument(instrument_name=n, short_instrument_name=n)
            attach(instrument, staff)
            score.append(staff)
        return score
