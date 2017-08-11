import abjad
from calliope import bubbles, machines

# TO DO MAYBE... rethink this naming (i.e. could cause confusion/conflict with calliope.Line)?
class Line(machines.EventMachine):
    child_types = (machines.Phrase, machines.Cell, machines.Event,)

    # TO DO: would be awesome to implement these!
    # auto_split_rests = True
    # auto_split_beams = True
    # auto_split_notes = True

    def replace_multimeasure_rests(self, music):
        """
        TO DO EVENTUALLY... probably some more elegant way to do this, but for now this works
        """
        if self.time_signature:
            measure_length = abjad.Duration(self.time_signature)
        else:
            # if no time signature specified, then this gets the pair for the duration of the first measure:
            measure_length = sum([abjad.Duration(i) for i in self.get_metrical_durations()[0]])

        leaves = abjad.select(music).by_leaf()
        rest_measures = 0
        measure_duration_tally = abjad.Duration(0)
        
        measure_has_only_rests = True # assume innocent until proven guilty
        measure_rests_to_replace = []
        rests_to_replace = []

        leaves_length = len(leaves)
        # print(music)
        for i,l in enumerate(leaves):
            
            measure_duration_tally += l.written_duration
            
            if isinstance(l, abjad.Rest) and measure_has_only_rests:
                measure_rests_to_replace.append(l)
            else:
                measure_has_only_rests = False

            if measure_duration_tally==measure_length:
                # if we're at the end of the line or this measure has notes, then maybe we need to add multimeasure rest beforehand
                # and then go and set rests_length back to 0
                if measure_has_only_rests:
                    rests_to_replace += measure_rests_to_replace
                    rest_measures += 1
                if i==leaves_length-1 or not measure_has_only_rests:
                    # then, add multimeasure rest, if > 0
                    if rest_measures > 0:
                        # print("MUTATE TO ADD REST %s/%s * %s" % (measure_length.pair[0], measure_length.pair[1], rest_measures) )
                        my_multimeasure_rests = abjad.Container("R1 * %s/%s * %s" % (measure_length.pair[0], measure_length.pair[1], rest_measures))
                        abjad.mutate(rests_to_replace).replace(my_multimeasure_rests)
                    rests_to_replace = []
                    rest_measures = 0

                # this measure is done, so set duration tally back to 0,
                # assume all rests in measure, and set rests in measure list back to empty
                # (all for the following measure):
                measure_duration_tally = abjad.Duration(0)
                measure_has_only_rests = True
                measure_rests_to_replace = []

    def process_rhythm_music(self, music, **kwargs):
        super().process_rhythm_music(music, **kwargs)
        self.replace_multimeasure_rests(music)

class LineBlock(machines.Block):
    # TO DO... implement this better... 
    child_types = (Line,)
    # is_simultaneous = True
    pass