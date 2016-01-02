from abjad import *

from _settings import PROJECT_PATH

import json
from copy import deepcopy

class GlobalMaterial(dict):
    data_path = PROJECT_PATH + "/ly_material"

    def __init__(self):
        self.loaded = set()

    # @staticmethod
    # def update_recursive(to_dict, from_dict):
    #     for key, value in from_dict.items():
    #         if isinstance(value, dict):
    #             to_dict[key] = Material.update_recursive(value, to_dict.get(key, {}))
    #         else:
    #             to_dict[key] = deepcopy(from_dict[key])
    #     return to_dict


    # def update(self, from_dict):
    #     Material.update_recursive(self, from_dict)


    def load(self, name, key_name=None, path=None, *args, **kwargs):
        print("LOADING MATERIAL: " + name)
        key_name = key_name or name

        path = path or self.data_path
        file_path = path + "/" + name + ".ly"

        if not key_name in self or not isinstance(self[key_name], dict):
            self[key_name] = GlobalMaterial()
        
        with open(file_path) as data_file:    
            material_string = data_file.read()
        
        l = material_string.split("=")
        l2 = [tok.rsplit("}", 1) for tok in l ]
        l3 = [item.strip() for sublist in l2 for item in sublist][:-1]

        # l3 = sum(l2, [])
        # l3 = l2
        # print(l3)

        material = {}

        for i, tok in enumerate(l3):
            if i % 2 == 0:
                material[tok] = l3[i+1] + " }"

            # print(material_string)
        self[key_name].update(material)

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

GLOBAL_MATERIAL = GlobalMaterial()

