import inspect
import abjad
from calliope import bubbles

# TO DO... rethink the organization of these classes

class Wrap(bubbles.Bubble):
    """
    creates a new container/bubble around the inner bubble
    """
    def __init__(self, music_bubble=None, **kwargs):
        self.music_bubble = lambda : music_bubble
        super().__init__(**kwargs)

    def music(self, **kwargs):
        my_music = self.music_container()
        bubble = self.music_bubble()
        if isinstance(bubble, bubbles.Bubble): # just as a precaution
            my_music.append( bubble.blow() )
        return my_music


class Voice(Wrap):
    is_simultaneous = None
    container_type = abjad.Voice

class Staff(Wrap):
    is_simultaneous = None
    container_type = abjad.Staff
    instrument = None
    clef = None

    def after_music(self, music, **kwargs):
        if self.instrument:
            abjad.attach(self.instrument, music)
        if self.clef:
            clef_obj = abjad.Clef(self.clef)
            abjad.attach(clef_obj, music)
        super().after_music(music, **kwargs)

    def show(self):
        self.show_pdf()

class RhythmicStaff(Staff):
    context_name="RhythmicStaff"
    clef="percussion"

class BubbleGridMatch(bubbles.Bubble):
    grid_bubble=None

    def __init__(self, grid_bubble=None, **kwargs):
        # set the grid bubble for any sub-bubbles (if not already defined) ... that way music bubbles passed to score
        # will be passed along to staff groups, and so on
        if grid_bubble:
            self.grid_bubble = grid_bubble
        super().__init__(**kwargs)
        BubbleGridMatch.set_grid_bubbles(self)

    @classmethod
    def set_grid_bubbles(cls, parent_bubble):
        if inspect.isclass(parent_bubble):
            sequence_method = parent_bubble.class_sequence
        else:
            sequence_method = parent_bubble.sequence
        for bubble_name in sequence_method():
            bubble = getattr(parent_bubble, bubble_name, None)
            if BubbleGridMatch.isbubble(bubble):
                bubble.grid_bubble = bubble.grid_bubble or parent_bubble.grid_bubble
                BubbleGridMatch.set_grid_bubbles(bubble)

    def music(self, **kwargs):
        my_music = self.music_container()
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            if hasattr(self, bubble_name):
                append_music = self.blow_bubble(bubble_name)
                if hasattr(self.grid_bubble, bubble_name):
                    append_music_inner = self.grid_bubble.blow_bubble(bubble_name)
                    append_music.append(append_music_inner)
                my_music.append(append_music)
        return my_music

class StaffGroup(BubbleGridMatch):
    is_simultaneous = None
    container_type = abjad.StaffGroup
    child_types=(Staff, BubbleGridMatch)
    instrument = None
    
    def after_music(self, music, **kwargs):
        if self.instrument:
            abjad.attach(self.instrument, music)
        super().after_music(music, **kwargs)

    def show(self):
        self.show_pdf()

class Piano(StaffGroup):
    class Piano1(Staff): pass
    class Piano2(Staff):
        clef = "bass"
    context_name = "PianoStaff"
    instrument=abjad.instrumenttools.Piano()

class Harp(StaffGroup):
    class Harp1(Staff): pass
    class Harp2(Staff):
        clef = "bass"
    context_name = "PianoStaff"
    instrument=abjad.instrumenttools.Harp()

class BubbleGridStaff(BubbleGridMatch, Staff):
    """
    creates a staff with a voice or voices inside of it
    """
    child_types=(Voice,) # needed? (throws exception otherwise... why?)
    instrument=None
    clef=None

class InstrumentStaffGroup(StaffGroup):
    def after_music(self, music, **kwargs):
        super().after_music(music, **kwargs)
        abjad.set_(music).systemStartDelimiter = "SystemStartSquare"

