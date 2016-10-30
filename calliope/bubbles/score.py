import inspect
import abjad
from calliope import tools, bubbles

class Score(bubbles.BubbleGridMatch):
     # NOTE: abjad.Score.__init__ does not take is_simultaneous as an argument,
    # so it needs to be set to be set to None here
    is_simultaneous = None

    container_type=abjad.Score
    child_types=(bubbles.Staff, bubbles.StaffGroup)
    # TO DO... the following are no longer used... kep them?
    hide_empty = False 
    title = ""

    def after_music(self, music, **kwargs):
        super().after_music(music, **kwargs)
        # music.add_final_bar_line()
        self.info("finished creating abjad music container object for the score")


class AutoScore(Score):

    def __init__(self, module, **kwargs):
        super().__init__(**kwargs)
        self.module = module

class ModuleBubble(bubbles.Bubble):
    module = None
    is_simultaneous = True

    def __init__(self, module, **kwargs):
        # for s in self.sequence():
        self.module = module
        for n, o in self.module.__dict__.items():
            # note, needing to append to __ordered__ here because this has already been set by __new__
            if bubbles.Line.isbubble(o):
                setattr(self, n, o)
                self.__ordered__.append(n)
        super().__init__(**kwargs)


class ModuleScoreSequence(Score):
    modules = ()

    def music(self, **kwargs):
        pass

    def blow_bubble(self, bubble_name):
        """
        execute for each bubble attribute to add that bubble's music to the main bubble's music.
        NOTE that classes that inherit from GridSequence should NOT override blow_bubble
        """
        bubble = getattr(self, bubble_name)
        if isinstance(bubble, Placeholder):
            bubble = Sequence(
                bubble_name=bubble_name, 
                container_type = bubble.container_type,
                context_name = bubble.context_name,
                grid_sequence=self.grid_sequence)
        return bubble.blow()