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

    def process_music(self, music, **kwargs):
        super().process_music(music, **kwargs)
        self.info("finished creating abjad music container object for the score")


class AutoScore(Score):

    # TO DO... add in stylesheet here
    def __init__(self, grid_bubble=None, *args, **kwargs):
        super().__init__(grid_bubble=grid_bubble, *args, **kwargs)
        if self.grid_bubble is not None:
            for bubble_name in self.grid_bubble.sequence():
                bubble = bubbles.Staff(
                    instrument=abjad.instrumenttools.Instrument(
                        instrument_name=bubble_name, 
                        short_instrument_name=bubble_name)
                    )
                self[bubble_name] = bubble

class ModuleBubble(bubbles.Bubble):
    module = None
    is_simultaneous = True

    @classmethod
    def class_sequence(self, **kwargs):
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


