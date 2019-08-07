import abjad, calliope

class PulseEvents(calliope.Transform):
    beats = 0.5

    def transform(self, selectable, **kwargs):

        for e in selectable.note_events:
            beats_tally = self.beats
            total_event_beats = e.beats

            if beats_tally < total_event_beats:
                e.beats = self.beats

            while beats_tally < total_event_beats:

                add_event_beats = min(total_event_beats - beats_tally, self.beats)
                # TO DO MAYBE: implement an insert after?

                e.parent.insert(e.my_index+1, e(beats=add_event_beats))

                beats_tally += add_event_beats
