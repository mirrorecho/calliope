import inspect
import abjad
from calliope import bubbles

# TO DO... rethink the organization of these classes

class Wrap(bubbles.Bubble):
    """
    creates a new container/bubble around the inner bubble
    """
    grid_bubble = None # needed for grid bubble matching

    def __init__(self, inner_bubble=None, **kwargs):
        self.get_inner_bubble = lambda : inner_bubble # TO DO... why the lambda?
        super().__init__(**kwargs)

    def music(self, **kwargs):
        my_music = self.music_container()

        # TO DO: why all this nonsense????
        inner_bubble = self.get_inner_bubble()
        if inner_bubble:
            my_music.append( self.inner_bubble().blow() )
        return my_music


class Voice(Wrap):
    is_simultaneous = None
    container_type = abjad.Voice

class Staff(Wrap):
    is_simultaneous = None
    container_type = abjad.Staff
    instrument = None
    clef = None

    def process_music(self, music, **kwargs):
        if self.instrument:
            abjad.attach(self.instrument, music)
        if self.clef:
            clef_obj = abjad.Clef(self.clef)
            abjad.attach(clef_obj, music)
        super().process_music(music, **kwargs)

    def show(self):
        self.show_pdf()

class RhythmicStaff(Staff):
    context_name="RhythmicStaff"
    clef="percussion"

class BubbleGridMatch(bubbles.Bubble):
    grid_bubble=None

    def __init__(self, grid_bubble=None, *args, **kwargs):
        # set the grid bubble for any sub-bubbles (if not already defined) ... that way music bubbles passed to score
        # will be passed along to staff groups, and so on
        kwargs["grid_bubble"] = grid_bubble
        super().__init__(*args, **kwargs)
        self.set_grid_bubbles(self)

    def set_grid_bubbles(self, parent_bubble):
        # TO DO... there might be a better way to iterate through all children...
        for child_bubble in parent_bubble.children:
            # print(child_bubble)
            child_bubble.grid_bubble = child_bubble.grid_bubble or parent_bubble.grid_bubble
            self.set_grid_bubbles(child_bubble)

    def child_music(self, child_bubble):
        return_music = super().child_music(child_bubble)
        if child_bubble.name in self.grid_bubble.sequence():
            return_music.append(
                self.grid_bubble.child_music( self.grid_bubble[child_bubble.name] )
                )
        return return_music

class StaffGroup(BubbleGridMatch):
    is_simultaneous = None
    container_type = abjad.StaffGroup
    child_types=(Staff, BubbleGridMatch)
    instrument = None
    
    def process_music(self, music, **kwargs):
        if self.instrument:
            abjad.attach(self.instrument, music)
        super().process_music(music, **kwargs)

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
    def process_music(self, music, **kwargs):
        super().process_music(music, **kwargs)
        abjad.set_(music).systemStartDelimiter = "SystemStartSquare"

