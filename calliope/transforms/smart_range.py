import abjad
import calliope

class SmartRange(calliope.Transform):
    """
    keeps pitches within a given range, minimizing jumps
    """

    smart_range = (0,24)
    # NOTE: only works if...?

    def transform(self, selectable, **kwargs):
        def pairwise(iterable):
            it = iter(iterable)
            a = next(it, None)
            for b in it:
                yield (a, b)
                a = b

        my_range = abjad.PitchRange.from_pitches(*self.smart_range)
        non_rest_list = list(selectable.note_events)

        # TO DO: make work for chords!
        for previous_event, event in pairwise([non_rest_list[0]] + non_rest_list):
            pitches_in_range = [p.number for p in my_range.voice_pitch_class(event.pitch)]
            event.pitch = min(pitches_in_range, key=lambda x: abs(x-previous_event.pitch) )