# -*- encoding: utf-8 -*-

import abjad
from calliope import bubbles
from copper import machines
# from copper.machines.tools import IndexedData as ID # just to avoid a lot of typing

class LeafData(machines.AttachmentTagData, machines.Tree):
    # TO DO... how/whether to use this????
    original_duration = 0
    ticks = 0
    rest = False

class LogicalTieData(machines.AttachmentTagData, machines.Tree):
    original_duration = 0
    ticks = 0
    rest = False

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

class ParentAttachmentTagData(machines.AttachmentTagData, machines.Tree):
    @property
    def ticks(self):
        return sum([l.ticks for l in self.leaves])

    @property
    def ticks_before(self):
        if self.children:
            return self.children[0].ticks_before
        return 0

    @property
    def ticks_after(self):
        return self.ticks_before + self.ticks

class EventData(ParentAttachmentTagData):
    # TO DO... should every logical tie in an event have the same pitch?

    pitch = 0 # note, this could be set to a list/tuple to indicate a chord
    original_pitch = 0 # just a way to track what's going on if pitch is transposed
    respell = None # set to "sharps" or "flats" 
    children_type = LogicalTieData
    from_line = None # used in FragmentLine for EventData that's copied from another line (tracks where it's copied from)

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


class CellData(ParentAttachmentTagData):
    # pitch_segment = None
    # rhythm_segment = None
    # pitch_reverse = False
    # rhythm_reverse = False
    # rhythm_multiplier = None
    children_type = EventData


class PhraseData(ParentAttachmentTagData):
    children_type = CellData

class TreeData(ParentAttachmentTagData):
    children_type = PhraseData