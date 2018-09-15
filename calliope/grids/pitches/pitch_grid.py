import random
import numpy as np
import pandas as pd
import abjad
import calliope

class PitchGrid(calliope.GridBase):
    pitch_ranges = None
    # auto_move_into_ranges = False # TO DO... use this?

    def move_into_ranges(self):
        if self.pitch_ranges is not None:
            num_rows, num_cols = self.pitch_ranges.shape
            for r in self.range_rows:
                for c in self.range_cols:

                    pitch_range = abjad.PitchRange.from_pitches(
                        *self.pitch_ranges.iat[r % num_rows, c % num_cols]
                        )

                    # TO DO: consider... always move to new random choice? Or only move if pitch not already in range?
                    my_pitch = random.choice(pitch_range.voice_pitch_class(self.data.iat[r, c])).number
                    # print(my_pitch)
                    self.data.iat[r, c] = my_pitch
        else:
            self.warn("Tried moving pitches into ranges, but pitch_ranges is None")
 

    def rearrange_try(self, depth):
        super().rearrange_try(depth)

        # if self.auto_move_into_ranges:

            # ???????? passable way to move pitches into matching octave
            # TO DO... ??????!!!!! WTF IS ALL THIS...?
            # for l in self.range_rows:
            #     for c in self.range_cols:
            #         if c == 0:
            #             if (self.data.iat[l, c+1] - self.data.iat[l, c]) < -6 and random.randrange(2) == 1:
            #                 self.data.iat[l, c] -= 12
            #             elif (self.data.iat[l, c+1] - self.data.iat[l, c]) > 6 and random.randrange(2) == 1:
            #                 self.data.iat[l, c] += 12
            #         elif c == self.num_columns-1:
            #             if (self.data.iat[l, c-1] - self.data.iat[l, c]) < -6 and random.randrange(2) == 1:
            #                 self.data.iat[l, c] -= 12
            #             elif (self.data.iat[l, c-1] - self.data.iat[l, c]) > 6 and random.randrange(2) == 1:
            #                 self.data.iat[l, c] += 12
            #         else:
            #             if (self.data.iat[l, c+1] + self.data.iat[l, c-1]) - (self.data.iat[l, c] * 2) < -12 and random.randrange(2) == 1:
            #                 self.data.iat[l, c] -= 12
            #             elif (self.data.iat[l, c+1] + self.data.iat[l, c-1]) - (self.data.iat[l, c] * 2) > 12 and random.randrange(2) == 1:
            #                 self.data.iat[l, c] += 12

        if self.pitch_ranges is not None:
            self.move_into_ranges()
            # print(self.data)

    def item_to_machine(self, item):
        return calliope.Event(pitch=item, beats=1)

    # TO DO... rethink
    # @classmethod
    # def row_list_from_bubble(cls, bubble):
    #     return [cls.item_from_bubble(e) for e in bubble.non_rest_events]

    # @classmethod
    # def item_from_bubble(cls, bubble):
    #     if hasattr(bubble, "pitch"):
    #         return abjad.NumberedPitch(bubble.pitch).number
    #     else:
    #         print("WARNING: bubble item has no pitch attribute for pitch grid")
    #         return 0
