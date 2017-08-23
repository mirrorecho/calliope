import random
import numpy as np
import pandas as pd
import abjad
import calliope

class PitchGrid(calliope.GridBase):
    to_bubble_type = calliope.Cell
    row_to_bubble_type = calliope.Cell
    pitch_ranges = ()
    auto_move_into_ranges = False

    def __init__(self, pitch_ranges=None, **kwargs):
        super().__init__(**kwargs)

        # self.dont_touch_pitches = None # [[]] # for future use
        self.pitch_ranges = pitch_ranges # TO DO... extrapolate last entry for total # of lines/columns
        
        # TO DO: re-enable auto ranges....?
        # self.auto_move_into_ranges = self.pitch_ranges is not None

        # self.octave_transpositions_allowed = True # TO DO: never used... implement?
        self.save_attrs.extend(["pitch_ranges"])


    def move_into_ranges(self):
        if self.pitch_ranges:
            for r in self.range_rows:
                for c in self.range_cols:

                    pitch_range = self.pitch_ranges.iat[r % len(self.pitch_ranges), c % len(self.pitch_ranges.columns)]
                    # TO DO: consider... always move to new random choice? Or only move if pitch not already in range?
                    self.data.iat[r, c] = random.choice(pitch_range.voice_pitch_class(self.data.iat[r, c])).number
        else:
            print("Tried moving pitches into ranges, but pitch_ranges is None")
 

    def rearrange_try(self, depth):
        super().rearrange_try(depth)

        # if self.auto_move_into_ranges:

            # ???????? passable way to move pitches into matching octave
            # TO DO... ??????!!!!! WTF IS ALL THIS...?
            # for l in range(self.num_lines):
            #     for c in range(self.num_columns):
            #         if c == 0:
            #             if (self.pitch_lines[l][c+1] - self.pitch_lines[l][c]) < -6 and random.randrange(2) == 1:
            #                 self.pitch_lines[l][c] -= 12
            #             elif (self.pitch_lines[l][c+1] - self.pitch_lines[l][c]) > 6 and random.randrange(2) == 1:
            #                 self.pitch_lines[l][c] += 12
            #         elif c == self.num_columns-1:
            #             if (self.pitch_lines[l][c-1] - self.pitch_lines[l][c]) < -6 and random.randrange(2) == 1:
            #                 self.pitch_lines[l][c] -= 12
            #             elif (self.pitch_lines[l][c-1] - self.pitch_lines[l][c]) > 6 and random.randrange(2) == 1:
            #                 self.pitch_lines[l][c] += 12
            #         else:
            #             if (self.pitch_lines[l][c+1] + self.pitch_lines[l][c-1]) - (self.pitch_lines[l][c] * 2) < -12 and random.randrange(2) == 1:
            #                 self.pitch_lines[l][c] -= 12
            #             elif (self.pitch_lines[l][c+1] + self.pitch_lines[l][c-1]) - (self.pitch_lines[l][c] * 2) > 12 and random.randrange(2) == 1:
            #                 self.pitch_lines[l][c] += 12

        if self.pitch_ranges:
            self.move_into_ranges()


    def item_to_bubble(self, item):
        return calliope.Event(pitch=item, beats=1)

    @classmethod
    def item_from_bubble(self, bubble):
        if hasattr(bubble, "pitch"):
            return bubble.pitch
        else:
            print("WARNING: bubble item has no pitch attribute for pitch grid")
            return 0
