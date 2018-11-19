import abjad
import calliope

# TO DO: consider renaming?
class Line(calliope.SegmentMixin, calliope.EventMachine):
    child_types = (calliope.Phrase, calliope.Cell, calliope.Event,)
    select_property = "lines"

    # TO DO: would be awesome to implement these!
    # auto_split_rests = True
    # auto_split_beams = True
    # auto_split_notes = True

    def replace_multimeasure_rests(self, music, measure_duration=(4,4)):
        """

        """

        # # TO DO EVENTUALLY... some more elegant way to do this, but for now this works
        # # LOOK INTO: abjad's rewrite meter (which should do anyway for the duration)
        # #.... would look somethind like this:
        # for shard in adbjad.mutate(music).split([(4,4)], cyclic=True):
        #     abjad.mutate(shard).rewrite_meter((4,4))

        # for shard in adbjad.mutate(music).split([(4,4)], cyclic=True):
        #     if all(isinstance(x, abjad.Rest) for x in shard):
        #         abjad.mutate(shard).replace(abjad.MultimeasureRest(shard))



        # TO DO WARNING... SHOULD READ IN TIME SIGNATURE
        measure_length = abjad.Duration( measure_duration )

        leaves = abjad.select(music).leaves()
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
                # print("YOYO")
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
