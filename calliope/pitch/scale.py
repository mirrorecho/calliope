import math
import abjad
import calliope

class Scale(calliope.CalliopeBase):
    """ 
    An abstract representation of a scale. Does not necessarily need
    to span a 12-semitone "octave".
    """

    root = 0 # default is middle C
    steps = (0,2,4,5,7,9,11,12) # must start on 0, default is diatonic
    print_kwargs = ("root", "steps")

    # TO DO: add methods to swap between iterables of degrees and pitches

    # TO DO: add slicing


    @property
    def octave_size(self):
        """ Gets the size in semitones of the span of the "octave". """
        return self.steps[-1]

    @property
    def num_steps(self):
        return len(self.steps)-1

    def __init__(self, pitches=None, **kwargs):
        super().__init__(**kwargs)
        if pitches:
            unrooted_steps = sorted(set(pitches)) # removes dupes and sorts
            self.root = unrooted_steps[0]
            self.steps = tuple([ p-self.root for p in  unrooted_steps])


    def __getitem__(self, arg):
        
        if isinstance(arg, int):
            my_octave_and_step = divmod(arg, self.num_steps)
            return (my_octave_and_step[0] * self.octave_size) + self.steps[my_octave_and_step[1]] + self.root

        elif isinstance(arg, slice):
            print("Scale slicing not implemented yet!")
        else:
            raise(TypeError("Scale indices must be integers or slices."))


    def pitch_transpose_within(self, pitch, steps):
        return self[self.index(pitch)+steps]

    def pitch_change_scale(self, pitch, new_scale, steps=0):
        return new_scale[self.index(pitch)+steps]

    def index(self, pitch):
        """ Gets index for a pitch number. If pitch is not found in the scale,
        then rounds up."""
        
        rooted_pitch = pitch - self.root
        rooted_octave_and_pitch_class = divmod(rooted_pitch, self.octave_size)
        rooted_pitch_class_index = next(i for i, p in enumerate(self.steps) if p>=rooted_octave_and_pitch_class[1])

        return (rooted_octave_and_pitch_class[0] * self.num_steps) + rooted_pitch_class_index


