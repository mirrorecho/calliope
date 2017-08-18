import calliope

class TallyCircleOfFifthsRange(calliope.TallyBase):
    def __init__(self, fifth_range_max=7, over_range_multiplier=-44):
        self.fifth_range_max = fifth_range_max
        self.over_range_multiplier = over_range_multiplier
                
    def tally_line(self, grid, row_index):
        #QUESTION... what about

        line = grid.pitch_lines[row_index]

        # just to keep things concise, n = the number of columns
        n = grid.num_columns
        
        # gets the index of each pitch on the circle of 5ths (with C as 0, G as 1, etc.)
        fifths_away = [(line[c] * 7) % 12 for c in range(n)]

        # sorts the circle of fifths indeces used (so we have a picture of what that distribution is like)
        fifths_away_sorted = copy.deepcopy(fifths_away)
        fifths_away_sorted.sort()

        fifths_away_sorted_gaps = [
                    (fifths_away_sorted[0] - fifths_away_sorted[n-1]) % 12 if i==0 
                    else fifths_away_sorted[i] - fifths_away_sorted[i-1]  for i in range(n)
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

            for i in range(n):
                fifth_distance_over = (fifths_away[i] - mid_fifths_range) % 12
                fifth_distance_under = (mid_fifths_range - fifths_away[i]) % 12
                fifth_min_distance = min(fifth_distance_over, fifth_distance_under)
                # print(fifth_min_distance)
                if fifth_min_distance > ((self.fifth_range_max - 1) / 2):
                    badness = fifth_min_distance - ((self.fifth_range_max - 1) / 2)
                    grid.add_tally(row_index, i, badness * self.over_range_multiplier)