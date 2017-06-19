# -*- encoding: utf-8 -*-

import abjad
from calliope import structures, bubbles

# TO DO... re-add TagSet once this is properly implemented
# TO DO... how/whether to use this????
# class LeafData(structures.TagSet, structures.Tree):
class LeafData(structures.Tree):
    original_duration = 0
    ticks = 0
    rest = False

# TO DO... re-add TagSet once this is properly implemented
# class MachineBubbleBase(structures.TagSet, structures.Tree, bubbles.LineTalea):
class MachineBubbleBase(bubbles.LineTalea, structures.Tree):

    name = None

    def __init__(self, name=None, **kwargs):
        if name:
            self.name=name
        super().__init__(**kwargs) 
        structures.Tree.__init__(self) # TO DO: necessary???

    def __call__(self, name=None, **kwargs):
        return_bubble = copy.copy(self) # TO DO... consider deep copy here
        if name:
            return_bubble.name = name
        for name, value in kwargs.items():
            setattr(return_bubble, name, value)

    def set_data(self, *args, **kwargs):
        """
        by default, appends bubbles in the sequence as children in the tree
        can also be overriden or used as a hook for setting/manipulating attributes
        """
        # TO DO... maybe this should just be in __init__????
        for bubble_name in self.sequence():
            # print(bubble_name)
            # TO DO: WARNING: will this work for class-based bubbles
            bubble = getattr(self, bubble_name)
            self.append(bubble)


    def get_signed_ticks_list(self, append_rest=False):
        # TO DO.. there's probably a more elegant one-liner for this!
        return_list = []
        for l in self.leaves:
            return_list.extend(l.get_signed_ticks_list())
        
        if append_rest:
            ticks_end = self.ticks
            metrical_duration_ticks = self.get_metrical_duration_ticks()
            if metrical_duration_ticks > ticks_end:
                return_list.append(int(ticks_end - metrical_duration_ticks))

        return return_list

    def process_rhythm_music(self, music, **kwargs):
        super().process_rhythm_music(music, **kwargs)

    @property
    def ticks(self):
        return sum([l.ticks for l in self.leaves])

    @property
    def beats(self):
        return self.ticks / self.rhythm_default_multiplier

    @property
    def ticks_before(self):
        if self.children:
            return self.children[0].ticks_before
        return 0

    @property
    def ticks_after(self):
        return self.ticks_before + self.ticks

    @property
    def logical_ties(self):
        return self.leaves



class LogicalTieData(MachineBubbleBase):
    # original_duration = 0 # TO DO: USE THIS?
    ticks = 0
    pitch = None # if None, defaults to Event's pitch
    rest = False

    def set_data(self, beats=None, pitch=None, **kwargs):
        self.beats = beats
        self.pitch = pitch

    def get_signed_ticks_list(self):
        return [self.ticks if not self.rest else 0 - self.ticks]

    @property
    def beats(self):
        return super().beats

    @beats.setter
    def beats(self, value):
        self.ticks = int(value * self.rhythm_default_multiplier)

    @property
    def use_ancestor_attachments(self):
        return self.is_first_non_rest

    @property
    def is_first_non_rest(self):
        return self is self.parent.first_non_rest

    @property
    def ticks_before(self):
        running_count = 0
        for l in self.root.leaves:
            if l is self:
                return running_count
            running_count += l.ticks
    @property
    def ticks_after(self):
        return self.ticks_before + self.ticks


class Event(MachineBubbleBase):

    pitch = 0 # note, this could be set to a list/tuple to indicate a chord
    original_pitch = 0 # just a way to track what's going on if pitch is transposed
    respell = None # set to "sharps" or "flats" 
    child_types = (LogicalTieData,)
    from_line = None # used in FragmentLine for EventData that's copied from another line (tracks where it's copied from)

    def __init__(self, name=None, beats=None, pitch=None, tie_name="tie", *args, **kwargs):
        super().__init__(name, **kwargs)
        if beats:
            child_tie = self.branch(tie_name)
            setattr(self, tie_name, child_tie)
            child_tie.set_data(beats=beats, **kwargs)
        if pitch:
            self.pitch = pitch

    # def set_data(self, beats, pitch=0, **kwargs):
    #     self.pitch = pitch
    #     child_tie = self.branch()
    #     child_tie.set_data(beats=beats, **kwargs)

    @property
    def first_non_rest(self):
        for l in self.children:
            if not l.rest:
                return l

    @property
    def last_non_rest(self):
        for l in self.children[::-1]:
            if not l.rest:
                return l

    def remove_bookend_rests(self):
        if self.children:
            if self.children[0].rest:
                self.pop(0)
        if self.children:
            if self.children[-1].rest:
                self.pop(-1)


class Cell(MachineBubbleBase):
    # pitch_segment = None
    # rhythm_segment = None
    # pitch_reverse = False
    # rhythm_reverse = False
    # rhythm_multiplier = None
    child_types = (Event,)


class Phrase(MachineBubbleBase):
    child_types = (Cell,)

class XDefinition(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
