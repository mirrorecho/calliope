from collections import Mapping
from copy import deepcopy
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


class Bubble(Container):

    def __init__(self, 
            name="a-bubble", 
            *args, **kwargs
            ):
        super().__init__(*args, **kwargs)
        self.name=name
        self.is_simultaneous = True

        self.voices = {} # necessary?
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
            mybubble.use_voices(b.voices)
        for b in bubbles:
            for n, v in b.voices.items():
                mybubble.voices[n].extend(v)
        return mybubble

    def rename_voice(self, old_name, new_name):
        self.voices[new_name] = self.voices.pop(old_name)
        self.voices[new_name].name = new_name

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
    def use_voices(self, names, *args, **kwargs):
        for v in names:
            self.use_voice(v)

    def use_voice(self, name, *args, **kwargs):
        if name not in self.voices:
            voice = Context(name=name, context_name="Voice", *args, **kwargs)
            self.append(voice)
            self.voices[name] = voice

    # TO DO... make this better
    def make_staves(self):
        for i, v in enumerate(self.voices):
            staff = Staff(name=v+"-staff")
            staff_voice = Context(name=v, context_name="Voice")
            staff.append(staff_voice)
            self.insert(i, staff)
