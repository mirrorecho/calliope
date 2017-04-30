class PitchesReverse(object):
    pitch_reverse=()

    def set_segment(self, segment, **kwargs):
        super().set_segment(segment, **kwargs)
        if segment.my_index in self.pitch_reverse:
            segment.pitch_segment = segment.pitch_segment[::-1]
            segment.pitch_reverse = True

class RhythmsReverse(object):
    rhythm_reverse=()

    def set_segment(self, segment, **kwargs):
        super().set_segment(segment, **kwargs)
        if segment.my_index in self.rhythm_reverse:
            segment.rhythm_segment = segment.rhythm_segment[::-1]
            segment.rhythm_reverse = True