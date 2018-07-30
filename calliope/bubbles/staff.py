import inspect
import abjad
import calliope

class Voice(calliope.Bubble):
    is_simultaneous = False
    container_type = abjad.Voice

class Staff(calliope.Bubble):
    is_simultaneous = False
    container_type = abjad.Staff
    instrument = None
    clef = None

    def process_music(self, music, **kwargs):
        
        # needed for horizontal brackets:
        music.consists_commands.append('Horizontal_bracket_engraver')

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

# TO DO: rethink this...
# class BubbleGridMatch(calliope.Bubble):
#     grid_bubble=None

#     def __init__(self, grid_bubble=None, *args, **kwargs):
#         # set the grid bubble for any sub-bubbles (if not already defined) ... that way music bubbles passed to score
#         # will be passed along to staff groups, and so on
#         kwargs["grid_bubble"] = grid_bubble
#         super().__init__(*args, **kwargs)
#         self.set_grid_bubbles(self)

#     def set_grid_bubbles(self, parent_bubble):
#         # TO DO... there might be a better way to iterate through all children...
#         for child_bubble in parent_bubble.children:
#             # print(child_bubble)
#             child_bubble.grid_bubble = child_bubble.grid_bubble or parent_bubble.grid_bubble
#             self.set_grid_bubbles(child_bubble)

#     def child_music(self, child_bubble):
#         return_music = super().child_music(child_bubble)
#         if child_bubble.name in self.grid_bubble.sequence():
#             return_music.append(
#                 self.grid_bubble.child_music( self.grid_bubble[child_bubble.name] )
#                 )
#         return return_music

class CopyChildrenBubble(calliope.Bubble):

    def __init__(self, copy_children_from=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # TO DO: consider... is __init__ the best place for this?
        # maybe it should be called from music() instead?
        # self.info()
        self.set_children(self, copy_children_from)

    def set_children(self, parent_bubble, copy_children_from):
        # TO DO... there might be a better way to iterate through all children...
        if copy_children_from:
            if isinstance(copy_children_from, calliope.MatchSequence) and not copy_children_from.is_simultaneous:
                copy_children_from = copy_children_from.get_inverted()
            for child_bubble in parent_bubble.children:
                if isinstance(child_bubble, CopyChildrenBubble):
                    self.set_children(child_bubble, copy_children_from)
                else:
                    try:
                        # self.info(child_bubble)
                        child_bubble.append(  copy_children_from[child_bubble.name] )
                    except:
                        self.warn("""tried appending child music, but %s has no child named '%s'""" 
                            % (copy_children_from.name, child_bubble.name))
                    




class StaffGroup(CopyChildrenBubble):
    is_simultaneous = True
    container_type = abjad.StaffGroup
    child_types=(Staff, CopyChildrenBubble)
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
    instrument=abjad.Piano()

class Harp(StaffGroup):
    class Harp1(Staff): pass
    class Harp2(Staff):
        clef = "bass"
    context_name = "PianoStaff"
    instrument=abjad.Harp()

class StaffWithVoices(CopyChildrenBubble, Staff):
    is_simultaneous = True
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

