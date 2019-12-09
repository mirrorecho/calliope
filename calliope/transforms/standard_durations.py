import abjad
import calliope

class StandardDurations(calliope.Transform):
    standard_duration = 1
    min_duration = 0.5
    """
    Extends / shortends durations to conform to standard duration
    increments.
    """

    def transform(self, selectable, **kwargs):
        beat_counter = 0

        for e in list(selectable.events):
            old_beats = e.beats
            new_beats = old_beats

            if not e.rest:

                event_duration_offset = (
                    (beat_counter/self.min_duration) % 
                    (self.standard_duration/self.min_duration)
                    ) * self.min_duration

                new_beats = self.standard_duration - event_duration_offset
                extra_beats = old_beats - new_beats
                next_sib = e.tree_sib(1)
                # print(e, event_duration_offset, new_beats, extra_beats )
                
                if old_beats > new_beats:
                    e.beats = new_beats
                    if next_sib and next_sib.rest:
                        setattr(next_sib, "new_rest_beats", next_sib.beats + extra_beats)
                    else:
                        e.parent.insert(e.my_index+1, 
                            calliope.Event(beats=0-extra_beats))
                elif old_beats < new_beats:
                    if not next_sib or next_sib.rest:
                        e.beats = new_beats
                    if next_sib and next_sib.rest:
                        setattr(next_sib, "new_rest_beats", next_sib.beats - abs(extra_beats))
            
            elif (new_rest_beats := getattr(e, "new_rest_beats", None)) is not None:
                if new_rest_beats <= 0:
                    e.parent.remove(e)
                else:
                    e.beats = 0 - new_rest_beats
            
            beat_counter += old_beats