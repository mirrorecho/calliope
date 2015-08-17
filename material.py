from settings import PROJECT_PATH

import json
from copy import deepcopy

class GlobalMaterial(dict):
    data_path = PROJECT_PATH + "/data"

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


    def load(self, name, key_name=None, path=None, *args, **kwargs):
        print("LOADING MATERIAL: " + name)
        key_name = key_name or name

        path = path or self.data_path
        file_path = path + "/" + name + ".json"

        if not key_name in self or not isinstance(self[key_name], dict):
            self[key_name] = GlobalMaterial()
        
        with open(file_path) as data_file:    
            data = json.load(data_file)
            self[key_name].update(data)

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

class Material(GlobalMaterial):

    def __init__(self, search_string):
        self.search_list = search_string.split(".")
        GLOBAL_MATERIAL.use(self.search_list[0])
        super().__init__()

    def get(self):
        my_material = GLOBAL_MATERIAL
        for m in self.search_list:
            if m not in my_material:
                print("WARNING: '" + m + "' does not exist in the material dictionary.")
                return None
            my_material = my_material[m]
        return(my_material)