import abjad
import calliope

class SmartRange(calliope.Transform):
    smart_range = (0,24)
    # NOTE: only works if...?

    def __init__(self, *args, **kwargs):
        self.smart_range = args or self.smart_range
        super().__init__(**kwargs)

    def transform_nodes(self, machine):
        def pairwise(iterable):
            it = iter(iterable)
            a = next(it, None)
            for b in it:
                yield (a, b)
                a = b

        my_range = abjad.PitchRange.from_pitches(*self.smart_range)
        
        non_rest_list = machine.note_events.as_list()

        for previous_event, event in pairwise([non_rest_list[0]] + non_rest_list):
            pitches_in_range = [p.number for p in my_range.voice_pitch_class(event.pitch)]
            event.pitch = min(pitches_in_range, key=lambda x: abs(x-previous_event.pitch) )