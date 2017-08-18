from calliope import structures

class RhythmsBroken(object):
    """
    Machine mixin to lenghten notes or add rests to a segment. It's specifically set up to lenghen any duration in the defined
    segment where the original relative duration > 1 (the idea being that long notes can be extended, but others cannot)
    """
    breaks = None # Indexed Data with the the indices of the breaks and # of relative duration units to add, or, if negative, the length of the rest to add

    def __init__(self, **kwargs):
        self.breaks = self.breaks or ID() # defaults multipliers to 1
        super().__init__(**kwargs)

    def set_logical_ties(self, event, **kwargs):
        super().set_logical_ties(event, **kwargs)
        segment_index = event.parent.my_index

        if segment_index in self.breaks.keylist() and any([l.original_duration > 1 for l in event.children]):
            break_signed_ticks = int(self.breaks[segment_index] * self.rhythm_default_multiplier)
            # if a rest is being added, then it's added as a new logical tie:
            if break_signed_ticks < 0:
                insert_index = len(event.children) if event.parent.rhythm_reverse else 0 #insert rest after if segment reversed, else before
                event.insert(insert_index, calliope.LogicalTieData(ticks=abs(break_signed_ticks), rest=True )) # TO Do.. should we call set_logical_tie on this new logical tie data?
            else:
                # otherwise, the existing note is extended:
                if event.parent.rhythm_reverse:
                    logical_tie = event.last_non_rest
                else:
                    logical_tie = event.first_non_rest
                logical_tie.ticks += break_signed_ticks
