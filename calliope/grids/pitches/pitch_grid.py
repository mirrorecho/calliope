import random
import numpy as np
import pandas as pd
import abjad
import calliope

class PitchGrid(calliope.GridBase):
    pitch_ranges = None
    # auto_move_into_ranges = False # TO DO... use this?

    def move_into_ranges(self, pitch_try_number):
        sorted_column_indices = self.column_indices_by_tally() 

        if self.pitch_ranges is not None:
            num_rows, num_cols = self.pitch_ranges.shape
            for r in self.range_rows:
                for c in self.range_cols:
                    
                    current_pitch = self.data.iat[r, c]

                    pitch_range = abjad.PitchRange.from_pitches(
                        *self.pitch_ranges.iat[r % num_rows, c % num_cols]
                        )

                    # resets 
                    if (current_pitch not in pitch_range
                        or pitch_try_number < 3
                        or c in sorted_column_indices[int(num_cols/3)]):
                        
                        new_pitch = random.choice(pitch_range.voice_pitch_class(current_pitch)).number
                        self.data.iat[r, c] = new_pitch

        else:
            self.warn("Tried moving pitches into ranges, but pitch_ranges is None")

    # TO DO MAYBE: use this instead????
    #     def pairwise(iterable):
    #         it = iter(iterable)
    #         a = next(it, None)
    #         for b in it:
    #             yield (a, b)
    #             a = b

    #     non_rest_list = list(selectable.note_events)

    #     # TO DO: make work for chords!
    #     for i, (previous_event, event) in enumerate(pairwise([non_rest_list[0]] + non_rest_list)):
    #         my_range = abjad.PitchRange.from_pitches(*self.smart_range)
    #         pitches_in_range = [p.number for p in my_range.voice_pitch_class(event.pitch)]
    #         event.pitch = min(pitches_in_range, key=lambda x: abs(x-previous_event.pitch) )



    def rearrange_try(self, depth):
        super().rearrange_try(depth)

        pitch_try_number = random.randrange(0+depth,8+depth)

        if self.pitch_ranges is not None:
            self.move_into_ranges(pitch_try_number)

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

    def item_to_machine(self, item):
        return calliope.Event(pitch=item, beats=1)

    # TO DO... rethink
    # @classmethod
    # def row_list_from_bubble(cls, bubble):
    #     return [cls.item_from_bubble(e) for e in bubble.note_events]

    # @classmethod
    # def item_from_bubble(cls, bubble):
    #     if hasattr(bubble, "pitch"):
    #         return abjad.NumberedPitch(bubble.pitch).number
    #     else:
    #         print("WARNING: bubble item has no pitch attribute for pitch grid")
    #         return 0
