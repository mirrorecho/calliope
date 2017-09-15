import abjad
import calliope

class SmartRange(calliope.Transform):
    smart_range = (0,24)
    # NOTE: only works if

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
        
        pitched_logical_ties = [l for l in machine.logical_ties if not l.rest]
        pitched_logical_ties.insert(0, pitched_logical_ties[0])

        for previous_tie, tie in pairwise(pitched_logical_ties):
            pitches_in_range = [p.number for p in my_range.voice_pitch_class(tie.pitch)]
            tie.pitch = min(pitches_in_range, key=lambda x: abs(x-previous_tie.pitch) )