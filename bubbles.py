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
        print("LOADING MATERIAL: " + name)
        key_name = key_name or name

        file_path = path + "/" + name + ".json"
        if not key_name in self or not isinstance(self[key_name], dict):
            self[key_name] = Material()
        
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

GLOBAL_MATERIAL = Material()

class BubbleBase():
    def startup(self, *args, **kwargs):
        pass

    def before_blow(self, music, *args, **kwargs):
        pass

    def after_blow(self, music, *args, **kwargs):
        pass

    def bubble_wrap(self):
        return self

class Bubble(BubbleBase):
    container_type=Container
    name=None
    is_simultaneous=True
    bubble_types = (BubbleBase,)
    grid_sequence = ()
    material=()
    # using_material = () # necessary?

    # MAYBE TO DO... could be slick if all kwargs added to the bubble as attributes?
    def __init__(self, music_blow=None, *args, **kwargs):

        self.using_material = []
        my_material = Material()
        
        # a little hacky... but works well... 
        for c in reversed( type( self.bubble_wrap() ).mro()[:-2] ):
            # this calls the startup method on every base class
            if hasattr(c, "startup"):
                c.startup( self, *args, **kwargs)
            if hasattr(c, "material"):
                for m in reversed(c.material):
                    GLOBAL_MATERIAL.use(m)
                    # if m not in self.using_material: # necessary?
                    #     self.using_material.insert(0,m)
                    my_material.update(GLOBAL_MATERIAL[m])
        for name, value in my_material.items():
            setattr( self, name, value)

        if music_blow:
            if isinstance(music_blow, Bubble):
                self.music_blow = lambda : music_blow.blow()
            elif callable(music_blow):
                self.music_blow = lambda : music_blow()
            else:
                self.music_blow = lambda : music_blow # necessary???

        # MAYBE TO DO... it would be cleaner here to make bubbles for anything

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
        music.extend(self.bubble_wrap().music_blow())
        self.after_blow(music)
        return music

    def score(self, *args, **kwargs):
        """
        a quick way to get a full-fledged ajad score object for this bubble type...
        """
        score = Score()
        # TO DO... ADD SCORE TITLE (THE NAME OF THE CLASS)
        try:
            self.before_blow(score, *args, **kwargs)
        except:
            print("WARNING: error trying to run 'before_blow' on the auto-generated score. Some music may be missing...")

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
            self.after_blow(score, *args, **kwargs)
        except:
            print("WARNING: error trying to run 'before_blow' on the auto-generated score. Some music may be missing...")

        return score


    def show(self, *args, **kwargs):
        score = self.score(*args, **kwargs)
        show(score)

    def __str__(self):
        music = self.blow()
        return(format(music))


class Eval(Bubble):
    def __init__(self, cls, bubble_name):
        self.is_simultaneous = getattr(cls, bubble_name).is_simultaneous
        super().__init__( lambda : cls.blow_bubble(bubble_name) )

class Line(Bubble):
    is_simultaneous = False
    def __init__(self, music_blow=None, material=None, pitches=None, pitch_material=None, *args, **kwargs):
        # TO DO... DOES NOT WORK...!!!!!!!!!!!!
        my_music_blow = music_blow or (lambda : getattr(self, material))
        # TO DO... IMPLEMENT PITCH CONVERSION...
        super().__init__(my_music_blow, *args, **kwargs)

class BubbleWrap(Bubble):
    """
    a base class for bubbles that "wrap" other bubbles in order to modify or extend them (without going through the trouble
        of inheritence)
    """
    def __init__(self, bubble, *args, **kwargs):
        self.bubble_wrap = lambda : bubble.bubble_wrap()
        self.is_simultaneous = bubble.is_simultaneous
        super().__init__(bubble, *args, **kwargs)


class Transpose(BubbleWrap):
    def __init__(self, bubble, transpose_expr, *args, **kwargs):
        self.transpose_expr = transpose_expr
        super().__init__(bubble, *args, **kwargs)
    
    def after_blow(self, music, *args, **kwargs):
        super().after_blow(music, *args, **kwargs)
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

