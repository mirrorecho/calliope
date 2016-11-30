import abjad
from calliope import tools, bubbles


class LineTalea(bubbles.Line):
    """
    LineTalea is a Line bubble with a music method that ... 
    """

    metrical_durations = None  # ID(max=4, default=((1,1),))
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
        return self.get_rhythm_maker()([abjad.Duration(d) for d in self.metrical_durations.flattened()])

    def process_rhythm_music(self, music, **kwargs):
        pass

    def music(self, **kwargs):
        my_music = self.container_type( self.get_rhythm_music(**kwargs) )
        self.process_rhythm_music(my_music, **kwargs)
        return my_music



# --------------------------------------------------------------

tools.illustrate_me()