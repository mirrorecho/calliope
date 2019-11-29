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
        note_list = list(selectable.note_events)

        # TO DO: make work for chords!
        for previous_event, event in pairwise([note_list[0]] + note_list):
            pitches_in_range = [p.number for p in my_range.voice_pitch_class(event.pitch)]
            event.pitch = min(pitches_in_range, key=lambda x: abs(x-previous_event.pitch) )



class SmartRanges(calliope.Transform):
    """
    keeps pitches within a given range, minimizing jumps
    """

    smart_ranges = (
        (0,24),
        )
    # NOTE: only works if...?

    def transform(self, selectable, **kwargs):
        def pairwise(iterable):
            it = iter(iterable)
            a = next(it, None)
            for b in it:
                yield (a, b)
                a = b

        my_cyclic_range = abjad.CyclicTuple(self.smart_ranges)
        
        note_list = list(selectable.note_events)

        # TO DO: make work for chords!
        i = 0
        for previous_event, event in pairwise([note_list[0]] + note_list):
            my_range = abjad.PitchRange.from_pitches(*my_cyclic_range[i])
            if not event.is_chord:            
                pitches_in_range = [p.number for p in my_range.voice_pitch_class(event.pitch)]
                event.pitch = min(pitches_in_range, key=lambda x: abs(x-previous_event.pitch) )
            else:
                previous_pitch = previous_event.pitch if not previous_event.is_chord else previous_event.pitch[0]
                my_pitches = []
                # NOTE: doesn't work for octaves (will always collapse into unison!)
                for my_pitch in event.pitch:
                    pitches_in_range = [p.number for p in my_range.voice_pitch_class(my_pitch)]
                    my_pitches.append(min(pitches_in_range, key=lambda x: abs(x-previous_pitch) ))
                event.pitch = my_pitches

            i += 1

