import abjad
import calliope

# TO DO- consider: why live in libraries?

class PitchSequence(calliope.BaseMixin):
    # TO DO: implement as either numbers or abjad pitch objects
    intervals = ()
    keep_in_range = None # set to tupe with start pitch, stop pitch
    transpose = 0 
    base_sequence = None
    base_selections = (0,1) # e.g. (0,1) would be same
    

    @property
    def cyclic_length(self):
        """returns the length after which sequence repeats (usu. on new start pitch)
        ...which is the least common multiple of the lengths of all the intervals and base selections up the chain"""
        from functools import reduce

        def get_lengths(my_sequence=None, lengths=()):
            my_lengths = lengths or []
            my_sequence = my_sequence or self
            if my_sequence.base_sequence:
                my_lengths.append(len(my_sequence.base_selections) - 1)
            if my_sequence.intervals:
                my_lengths.append(len(my_sequence.intervals) - 1)
            if my_sequence.base_sequence:
                return get_lengths(my_sequence.base_sequence, my_lengths)
            else:
                return my_lengths

        lengths = get_lengths(self)

        def my_gcd(*numbers):
            """return the greatest common divisor of the given integers"""
            from fractions import gcd
            return reduce(gcd, numbers)

        def lcm(a, b):
            """returns the lowest common multiple."""    
            return (a * b) // my_gcd(a, b)

        return reduce(lcm, lengths, 1)



    def cyclic_at(self, attr_name, index):
        my_tuple = getattr(self, attr_name)
        loop_length = len(my_tuple) - 1
        base_item = my_tuple[index % loop_length]
        return base_item + (my_tuple[-1] - my_tuple[0]) * (index // loop_length)

    def pitch_at(self, index):
        pitch = self.transpose
        if self.base_sequence:
            selected_index = self.cyclic_at("base_selections", index)
            pitch += self.base_sequence[selected_index]
        if self.intervals:
            pitch += self.cyclic_at("intervals", index)
        if self.keep_in_range:
            pitch_range = abjad.PitchRange.from_pitches(*self.keep_in_range)
            if pitch not in pitch_range:
                voiced_pitches = pitch_range.voice_pitch_class(pitch)
                if pitch < pitch_range.start_pitch.number:
                    pitch = voiced_pitches[0].number
                else:
                    pitch = voiced_pitches[-1].number
        return pitch


    def __init__(self, *intervals, **kwargs):
        self.intervals = intervals
        self.setup(**kwargs)

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return self.pitch_at(arg)
        elif isinstance(arg, slice):
            start = arg.start or 0
            stop = arg.stop or 0
            step = arg.step or 1
            if start > stop and step > 0:
                step = 0 - step
            return tuple([self[i] for i in range(start, stop, step)])
        elif isinstance(arg, tuple):
            return tuple([self[a] for a in arg])
        else:
            raise IndexError('invalid index type')

    def __call__(self, *intervals, **kwargs):
        return PitchSequence(base_sequence=self, *intervals, **kwargs)

    def select(self, *selections, **kwargs):
        return PitchSequence(base_sequence=self, base_selections=selections, **kwargs)