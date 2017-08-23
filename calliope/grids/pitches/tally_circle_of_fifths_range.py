import calliope

class TallyCircleOfFifthsRange(calliope.TallyBase):
    fifth_range_max=7
    over_range_multiplier=-44
                
    def tally_row(self, grid, r):
        # TO DO EVENTUALLY... probalby a much more elegant way to do this with pandas...

        
        # a series the index of each pitch on the circle of 5ths (with C as 0, G as 1, etc.)
        fifths_away = grid.data.iloc[r].apply(lambda x: (x * 7) % 12)

        fifths_away_sorted = sorted(fifths_away)
        fifths_away_sorted_gaps = [
                    fifths_away_sorted[i] - fifths_away_sorted[i-1] for i in grid.range_cols
                    ]
        largest_gap = max(fifths_away_sorted_gaps)
        # print("-----------------------------------------------")

        # print("line:               " + str(line))
        # print("fifths away:        " + str(fifths_away))
        # print("fifths away sorted: " +  str(fifths_away_sorted))
        # print("gaps:               " + str(fifths_away_sorted_gaps))
        # print("-----------------------------------------------")
        # print("largest gap: " + str(largest_gap))

        if largest_gap <= (12 - self.fifth_range_max):
        
            largest_gap_at_fifth = fifths_away_sorted[fifths_away_sorted_gaps.index(largest_gap)]
            mid_fifths_range = (largest_gap_at_fifth + ((12-largest_gap) / 2)) % 12
            
            # print("largest gap before: " + str(largest_gap_at_fifth))
            # print("mid fifths range: " + str(mid_fifths_range))
            # print("-----------------------------------------------")
            # print()

            for c in grid.range_cols:
                fifth_distance_over = (fifths_away[c] - mid_fifths_range) % 12
                fifth_distance_under = (mid_fifths_range - fifths_away[c]) % 12
                fifth_min_distance = min(fifth_distance_over, fifth_distance_under)
                # print(fifth_min_distance)
                if fifth_min_distance > ((self.fifth_range_max - 1) / 2):
                    badness = fifth_min_distance - ((self.fifth_range_max - 1) / 2)
                    grid.add_tally(r, c, badness * self.over_range_multiplier)