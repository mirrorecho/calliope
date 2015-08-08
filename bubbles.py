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

class BubbleBase():
    pass

class Bubble(BubbleBase):
    container_type=Container
    name=None
    is_simultaneous=True
    bubble_types = (BubbleBase,)
    grid_sequence = ()

    def __init__(self, music_blow=None, *args, **kwargs):
        if music_blow:
            if isinstance(music_blow, Bubble):
                self.music_blow = lambda : music_blow.blow()
            elif callable(music_blow):
                self.music_blow = lambda : music_blow()
            else:
                self.music_blow = lambda : music_blow # necessary???

    def sequence(self, *args, **kwargs):
        # bubbles = [getattr(self,b) for b in dir(self) if isinstance(getattr(self,b), self.bubble_types)]
        # bubbles.sort(key=lambda x : x.order)
        bubbles = [b for b in dir(self) if isinstance(getattr(self,b), self.bubble_types)]
        return bubbles

    @classmethod
    def grid_set(cls):
        return_set = set()
        for g in cls.grid_sequence:
            return_set.add(g)
            return_set = return_set.union(g.grid_set())
        return return_set

    @classmethod
    def blow_bubble(cls, bubble_name):
        """
        execute for each bubble attribute to add that bubble's music to the main bubble's music
        """
        bubble = getattr(cls, bubble_name)
        if any([hasattr(g, bubble_name) for g in cls.grid_set()]):
            #... then this bubble attr needs to come from a grid...
            bubble_music = bubble.container_type(is_simultaneous=bubble.is_simultaneous)
            for g in cls.grid_sequence:
                bubble_music.extend( g.blow_bubble(bubble_name) )
            return bubble_music
        else:
            return bubble.blow()

    def music_blow(self, *args, **kwargs):
        if self.is_simultaneous is not None:
            music = self.container_type(is_simultaneous=self.is_simultaneous, *args, **kwargs)
        else:
            music = self.container_type(*args, **kwargs)
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            if hasattr(self, bubble_name):
               append_music = type(self).blow_bubble(bubble_name)
               music.append(append_music)
        return music

    def blow(self, *args, **kwargs):
        if self.is_simultaneous is not None:
            music = self.container_type(is_simultaneous=self.is_simultaneous, *args, **kwargs)
        else:
            music = self.container_type(*args, **kwargs)
        self.before_blow(music)
        music.extend(self.music_blow())
        self.after_blow(music)
        return music


    def before_blow(self, music, *args, **kwargs):
        pass

    def after_blow(self, music, *args, **kwargs):
        pass

class Eval(Bubble):
    def __init__(self, cls, bubble_name):
        super().__init__( lambda : cls.blow_bubble(bubble_name) )

class Line(Bubble):
    is_simultaneous = False

class BubbleStaff(Bubble):
    is_simultaneous = None
    container_type = Staff

class BubbleStaffGroup(Bubble):
    container_type = StaffGroup

class BubbleScore(Bubble):
    is_simultaneous = None
    container_type=Score
    bubble_types=(BubbleStaff, BubbleStaffGroup)


class BubbleOld():
    """
    a bubble represents a collection of musical material (e.g. pitches and rhythms)
    as well as a collection of generators that spit out  abjad contexts or containers
    """

    def __init__(self, 
            name="a-bubble", 
            is_simultaneous = False,
            container_type = Context,
            context_name="Context",
            *args, **kwargs
            ):
        super().__init__(*args, **kwargs)
        self.name=name
        self.is_simultaneous = is_simultaneous
        self.context_name = context_name

        self.blows = []

        # self.lines = OrderedDict() # necessary?
        self.material = Material()

        # a little hacky... but works well... this calls the music method on every base class
        for c in reversed( type(self).mro()[:-2] ):
            # print(c)
            if hasattr(c, "music"):
                c.music(self, *args, **kwargs)
                pass

    def blow(self, *args, **kwargs):
        if container_type == Context:
            music = Context(name=name, context_name=context_name)
        else:
            music = container_type(name=name)
        for m in methods:
            b = getattr(self, m)(*args, **kwargs)
            if isinstance(b, Bubble):
                music.append(b.blow(*args, **kwargs))
            else:
                music.append(b)
        return music



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
