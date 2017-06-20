import inspect
import abjad
from calliope import bubbles

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

    # TO DO... add in stylesheet here
    def __init__(self, gid_bubble=None, **kwargs):
        super().__init__(gid_bubble, **kwargs)
        if self.grid_bubble:
            for bubble_name in self.grid_bubble.sequence():
                bubble = bubbles.Staff(
                    instrument=abjad.instrumenttools.Instrument(
                        instrument_name=bubble_name, short_instrument_name=bubble_name)
                    )
                setattr(self, bubble_name, bubble)

class ModuleBubble(bubbles.Bubble):
    module = None
    is_simultaneous = True

    def sequence(self, **kwargs):
        bubble_info = sorted([
                (
                    inspect.getsourcefile(m[1]), 
                    inspect.getsourcelines(m[1])[1], 
                    m[0]
                ) if inspect.isclass(m[1])
                else 
                (
                    "z",
                    0,
                    m[0],
                )
                for m in inspect.getmembers(self.module, bubbles.Line.isbubble)
            ])
        return [b[2] for b in bubble_info]

    # def append_children(self):
    #     for n, o in self.module.__dict__.items():
    #         if bubbles.Line.isbubble(o):
    #             self[n] = o

    def __init__(self, module, **kwargs):
        super().__init__(**kwargs)
        self.module = module

