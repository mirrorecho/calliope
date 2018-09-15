import calliope

class PitchSequenceFactory(calliope.Factory):

    pitch_sequence = None
    pitch_sequence_index = self.pitch_sequence_index

    def get_pitches(self):
        return self.pitch_sequence[self.pitch_sequence_index : self.pitch_sequence_index+pitches_length],

    def fabricate(self):
                machine.append(calliope.Cell(
                    rhythm = rhythm,
                    pitches = pitch_sequence[pitch_sequence_index : pitch_sequence_index+pitches_length],
                    pitches_skip_rests = True
                ))