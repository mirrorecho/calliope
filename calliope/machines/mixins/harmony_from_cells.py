from calliope import machines

class HarmonyFromCells(object):

    def set_event(self, event, **kwargs):
        super().set_event(event, **kwargs)

        # unlike normal lines, events in harmonic lines cycle through pitch material at the segment level...
        setattr(event, "harmonic_pitch_segment_index", self.pitch_sequence[event.depthwise_index])
        # always sort chord pitches so that chord positions consistent
        unsorted_pitches = self.pitch_segments[event.harmonic_pitch_segment_index]
        event.original_pitch = sorted(unsorted_pitches)

        # TO DO EVENTUALLY... how to make this unaware of PitchesDisplaced?
        if isinstance(self, machines.PitchesDisplaced):
            pitch_displacement = self.get_pitch_displacement(**kwargs)

            # set pitches_before to the sum count of pitches in segments for previous events... we need this to calculate displacement
            pitches_before = 0
            for e in event.root.events:
                if e is event:
                    break
                # in case e isn't an harmnic event:
                if isinstance(e.pitch, (list, tuple)):
                    pitches_before += len(e.pitch)
                else:
                    pitches_before += 1

            # loop through pitches for this event to set displacement
            displaced_pitches = []
            for i, p in enumerate(unsorted_pitches):
                displacement_index = pitches_before + i
                displaced_pitches += [p + pitch_displacement.get_cumulative(displacement_index)]

            event.pitch = sorted(displaced_pitches) # always sort chord pitches so that chord positions consistent
        else:
            event.pitch = event.original_pitch

    def set_segment(self, segment, **kwargs):
        super().set_segment(segment, **kwargs)
        pitch_segment_index = None # resetting these here because doesn't apply to harmony (the entire)
        segment.pitch_segment = None
