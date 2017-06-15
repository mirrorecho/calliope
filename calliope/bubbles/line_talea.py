import abjad
from calliope import tools, bubbles


class LineTalea(bubbles.Line):
    """
    LineTalea is a Line bubble with a music method that ... 
    """

    metrical_durations = None  # ID(max=4, default=((1,1),))


    metrical_durations = ( (1,1),(1,1) ) # TO DO... rethink this with new machine structure

    rhythm_default_multiplier = 8
    rhythm_denominator = 32
    auto_split_rests = True
    auto_split_beams = True
    auto_split_notes = True


    def get_metrical_duration_ticks(self):
        """
        returns a number representing the total number of ticks in this line(relative to the object's rhythm_denominator)
        .... based on the defined metrical durations for this object
        """

        return int(sum([d[0]/d[1] for d in self.metrical_durations.flattened()]) * self.rhythm_denominator)

    def get_signed_ticks_list(self):
        """
        hook to return flattened list of all ticks, padded at the end based on the length, with rests as negative values
        """
        

        # DUMMY TEST VALUE.... 
        test_durations = [1, -1, 1, -1 ] 

        # TO DO... this is a bad place for this!!!!!!!!!!!!!!!!!!:
        self.metrical_durations = tools.IndexedData(max=4, default=((1,1),))
        
        return [d * self.rhythm_default_multiplier for d in test_durations]

        # TO ADD TO MACHINES:
        # ticks_list = []
        # for l in self.logical_ties:
        #     if isinstance(l, machines.LogicalTieData):
        #         ticks_list.append(l.ticks*-1 if l.rest else l.ticks)
        #     else:
        #         self.warn("item in data structure has no logical ties... skipping; output may be screwed up", l)
        # ticks_end = self.data.ticks
        # metrical_duration_ticks = self.get_metrical_duration_ticks()
        # if metrical_duration_ticks > ticks_end:
        #     ticks_list.append(int(ticks_end - metrical_duration_ticks))
        # return ticks_list

    def get_talea(self):
        return abjad.rhythmmakertools.Talea(self.get_signed_ticks_list(), self.rhythm_denominator)

    def get_rhythm_maker(self):
        return abjad.rhythmmakertools.TaleaRhythmMaker(
            talea=self.get_talea(),
            read_talea_once_only=True,
            # read_talea_once_only = False, # for testing only...
            # division_masks=division_masks, # for testing only...
            # extra_counts_per_division=extra_counts_per_division, # for testing only...
        )

    def get_rhythm_music(self, **kwargs):
        # return self.get_rhythm_maker()([abjad.Duration(d) for d in self.metrical_durations.flattened()])
        return self.get_rhythm_maker()([abjad.Duration(d) for d in self.metrical_durations])

    def replace_multimeasure_rests(self, music):
        """
        TO DO EVENTUALLY... probably some more elegant way to do this, but for now this works
        """
        if self.time_signature:
            measure_length = abjad.Duration(self.time_signature)
        else:
            # if no time signature specified, then this gets the pair for the duration of the first measure:
            measure_length = sum([abjad.Duration(i) for i in self.metrical_durations[0]])

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
        self.replace_multimeasure_rests(music)

    def music(self, **kwargs):
        my_music = self.container_type( self.get_rhythm_music(**kwargs) )
        self.process_rhythm_music(my_music, **kwargs)
        return my_music



# --------------------------------------------------------------

tools.illustrate_me()