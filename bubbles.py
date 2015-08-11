from collections import Mapping
from copy import deepcopy
from collections import OrderedDict
import json

from abjad import *



class GlobalMaterial(dict):
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
        print("LOADING MATERIAL: " + name)
        key_name = key_name or name

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

class BubbleBase():
    name=None
    container_type=Container
    is_simultaneous=False
    bubble_types = ()

    # MAYBE TO DO... could be slick if all kwargs added to the bubble as attributes?
    def __init__(self, music=None, *args, **kwargs):
        music = music or self.music
        if music is not None:
            if isinstance(music, BubbleBase):
                self.music = music.blow
            elif isinstance(music, Material):
                self.music = music.get
            elif callable(music):
                self.music = music
            else:
                self.music = lambda : music 

    def music_container(self, *args, **kwargs):
        if self.is_simultaneous is not None:
            return self.container_type(is_simultaneous=self.is_simultaneous, *args, **kwargs)
        else:
            return self.container_type(*args, **kwargs)

    # IMPLEMENT IF NEEDED...
    # def before_music(self, music, *args, **kwargs):
    #     pass

    def music(self, *args, **kwargs):
        print("WARNING... EMPTY MUSIC FUNCTION CALLED ON BUBBLE BASE")
        return self.music_container()

    def after_music(self, music, *args, **kwargs):
        pass

    def blow(self, *args, **kwargs):
        # IMPLEMENT IF BEFORE_MUSIC NEEDED, OTHERWISE KISS
        # my_music = self.music_container()
        # self.before_blow(my_music)
        # my_music.extend(self.bubble_wrap().music())
        my_music = self.bubble_wrap().music()
        self.after_music(my_music)
        return my_music

    def bubble_wrap(self):
        return self

    def __str__(self):
        music = self.blow()
        return(format(music))

class BubbleMaterial(Material, BubbleBase):

   def music(self, *args, **kwargs):
        my_music = self.music_container()
        my_music.append( self.get() )
        return my_music

class Bubble(BubbleBase):
    is_simultaneous=True
    bubble_types = (BubbleBase,)
    grid_sequence = ()

    def sequence(self, *args, **kwargs):
        # bubbles = [getattr(self,b) for b in dir(self) if isinstance(getattr(self,b), self.bubble_types)]
        # bubbles.sort(key=lambda x : x.order)
        seq_bubble = self.bubble_wrap()
        bubbles = [b for b in dir(seq_bubble) if isinstance(getattr(seq_bubble,b), self.bubble_types)]
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
            bubble_music = bubble.music_container()
            for g in cls.grid_sequence:
                bubble_music.extend( g.blow_bubble(bubble_name) )
            return bubble_music
        else:
            return bubble.blow()

    def music(self, *args, **kwargs):
        my_music = self.music_container()
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            if hasattr(self, bubble_name):
               append_music = type(self).blow_bubble(bubble_name)
               my_music.append(append_music)
        return my_music


    def score(self, *args, **kwargs):
        """
        a quick way to get a full-fledged ajad score object for this bubble type...
        """
        score = Score()
        # TO DO... ADD SCORE TITLE (THE NAME OF THE CLASS)
        # RE-ADD IF BEFORE_MUSIC NEEDED...`
        # try:
        #     self.before_music(score, *args, **kwargs)
        # except:
        #     print("WARNING: error trying to run 'before_music' on the auto-generated score. Some music may be missing...")

        def append_staff(name, bubble):
            staff = Staff(name=name)
            staff.append( bubble.blow() )
            instrument = instrumenttools.Instrument(instrument_name=name, short_instrument_name=name)
            attach(instrument, staff)
            score.append(staff)            

        if self.is_simultaneous:
            for i, b in enumerate(self.sequence()):
                bubble = Eval(type(self.bubble_wrap()), b)
                append_staff(b, bubble)
        else:
            append_staff(b.__class__.name, self)

        try:
            self.after_music(score, *args, **kwargs)
        except:
            print("WARNING: error trying to run 'after_music' on the auto-generated score. Some music may be missing...")

        return score


    def show(self, *args, **kwargs):
        score = self.score(*args, **kwargs)
        show(score)


class Eval(Bubble):
    def __init__(self, cls, bubble_name):
        self.is_simultaneous = getattr(cls, bubble_name).is_simultaneous
        super().__init__( lambda : cls.blow_bubble(bubble_name) )

class Line(Bubble):
    is_simultaneous = False

class BubbleWrap(Bubble):
    """
    a base class for bubbles that "wrap" other bubbles in order to modify or extend them (without going through the trouble
        of inheritence)
    """
    def __init__(self, bubble, *args, **kwargs):
        self.bubble_wrap = bubble.bubble_wrap
        self.is_simultaneous = bubble.is_simultaneous
        super().__init__(bubble, *args, **kwargs)


class Transpose(BubbleWrap):
    def __init__(self, bubble, transpose_expr, *args, **kwargs):
        self.transpose_expr = transpose_expr
        super().__init__(bubble, *args, **kwargs)
    
    def after_music(self, music, *args, **kwargs):
        super().after_music(music, *args, **kwargs)
        mutate(music).transpose(self.transpose_expr)

class BubbleStaff(Bubble):
    is_simultaneous = None
    container_type = Staff

class BubbleStaffGroup(Bubble):
    is_simultaneous = None
    container_type = StaffGroup

class BubbleScore(Bubble):
    is_simultaneous = None
    container_type=Score
    bubble_types=(BubbleStaff, BubbleStaffGroup)

