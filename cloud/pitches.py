from abjad import *

from calliope.work import Arrangement

import os
import random
import copy
import pickle

def get_diatonic_spread(pitch_line):
    pass

class TallyAppBase:

    # TO DO... some way to window/overlap to tally up longer things effectively?

    line_weights = None # could be used to make the tally count more at given spots
    column_weights = None # could be used to make the tally count more at given spots

    def __init__(self, line_weights=None, column_weights=None):
        self.line_weights=line_weights
        self.column_weights=column_weights

    def tally_line(self, cloud, line_index):
        pass

    def tally_column(self, cloud, column_index):
        pass

    def tally_pitch(self, cloud, line_index, column_index):
        pass

    def tally_pitch_across_lines(self, cloud, line_index, column_index, across_line_index):
        pass

    def tally_pitch_across_columns(self, cloud, line_index, column_index, across_colum_index):
        pass

class TallyMelodicIntervals(TallyAppBase):
    def __init__(self, interval_ratings=[], over_incremental_multiplier=None, by_pitch_class=False, bidirectional=True, line_weights=None, column_weights=None):
        self.interval_ratings = interval_ratings
        self.by_pitch_class = by_pitch_class
        self.bidirectional = bidirectional
        self.over_incremental_multiplier = over_incremental_multiplier
        super().__init__(line_weights=line_weights, column_weights=column_weights)

    def tally_pitch(self, cloud, line_index, column_index):
        # only makes sense starting from 2nd column:
        if column_index > 0:
            melodic_interval = cloud.pitch_lines[line_index][column_index] - cloud.pitch_lines[line_index][column_index-1]
            if self.bidirectional:
                melodic_interval = abs(melodic_interval)
            if self.by_pitch_class:
                melodic_interval = melodic_interval % 12
            for i,rating in self.interval_ratings:
                if melodic_interval == i:
                    cloud.add_tally(line_index, column_index, rating)
                    cloud.add_tally(line_index, column_index - 1, rating)
            # can be used to dock for big jumps
            if self.over_incremental_multiplier is not None:
                if abs(melodic_interval) > self.over_incremental_multiplier[0]:
                    over_rating = (abs(melodic_interval) - self.over_incremental_multiplier[0]) * self.over_incremental_multiplier[1]
                    cloud.add_tally(line_index, column_index, over_rating)


class TallyParallelIntervals(TallyAppBase):
    def __init__(self, interval_ratings=[(0,-100),], by_pitch_class=True, line_weights=None, column_weights=None):
        # default is to dock off 100 points for parallel unisons/octaves
        self.interval_ratings = interval_ratings
        self.by_pitch_class = by_pitch_class
        super().__init__(line_weights=line_weights, column_weights=column_weights)

    def tally_pitch_across_lines(self, cloud, line_index, column_index, across_line_index):
        # only makes sense starting from 2nd column:
        if column_index > 0:
            melodic_interval_1 = cloud.pitch_lines[line_index][column_index] - cloud.pitch_lines[line_index][column_index-1]
            melodic_interval_2 = cloud.pitch_lines[across_line_index][column_index] - cloud.pitch_lines[across_line_index][column_index-1]
            #if motion is parallel...
            if melodic_interval_1 == melodic_interval_2:
                interval = abs(cloud.pitch_lines[line_index][column_index] - cloud.pitch_lines[across_line_index][column_index])
                if self.by_pitch_class:
                    interval = interval % 12
                for i,rating in self.interval_ratings:
                    if interval == i:
                        cloud.add_tally(line_index, column_index, rating)
                        cloud.add_tally(across_line_index, column_index, rating)


class TallyCircleOfFifthsRange(TallyAppBase):
    def __init__(self, fifth_range_max=7, over_range_multiplier=-44):
        self.fifth_range_max = fifth_range_max
        self.over_range_multiplier = over_range_multiplier
                
    def tally_line(self, cloud, line_index):
        #QUESTION... what about

        line = cloud.pitch_lines[line_index]

        # just to keep things concise, n = the number of columns
        n = cloud.num_columns
        
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
                    cloud.add_tally(line_index, i, badness * self.over_range_multiplier)





class CloudPitches:

    def __init__(self, pitch_lines=None, filename=None, project=None, autoload=False):
        self.is_loaded = False

        if project is not None:
            self.project = project
        else:
            self.project = Project()

        # QUESTION ... better to use abjad's pitchtools.PitchArray()?
        if filename is None:
            filename = "cloud_data.dat"

        self.filepath = self.project.data_path + "/" + filename

        self.dont_touch_pitches = None # [[]] # for future use
        self.voice_ranges = [["[A3 A5]"]] # TO DO... extrapolate last entry for total # of lines/columns

        if pitch_lines is not None:
            self.pitch_lines = pitch_lines
        elif autoload and os.path.isfile(filepath):
            self.load()
        else:
            self.pitch_lines = [[]]

        self.init_data()

        self.tally_apps = []

        self.auto_move_into_ranges = True
        self.octave_transpositions_allowed = True

    def init_data(self, pitch_lines = None):
        if pitch_lines is not None:
            self.pitch_lines = pitch_lines
        self.num_lines = len(self.pitch_lines)
        self.num_columns = len(self.pitch_lines[0])
        self.reset_tally()
        try:
            if len(self.pitch_lines[0]) > 0:
                self.is_loaded = True
        except:
            pass

    def reset_tally(self):
        # fill initial tallies with 0s 
        # also QUESTION: is pitch-by-pitch tally enough? or should the entire lines/columns be tallied as well?
        self.tallies = [[0 for c in range(self.num_columns)] for l in range(self.num_lines)]
        # using a running total to avoid looping/summing up repeatedly to get total... does this even make a difference?
        self.tally_total = 0        

    def add_tally(self, line_index, column_index, value):
        self.tallies[line_index][column_index] += value
        self.tally_total += value

    def add_tally_app(self, tally_app):
        self.tally_apps.append(tally_app)

    def get_tallies(self):
        self.reset_tally()
        for line_index in range(self.num_lines):
            
            # line tallies for all apps
            for app in self.tally_apps:
                app.tally_line(self, line_index)
            
            for column_index in range(self.num_columns):
                
                if line_index == 0:
                    #column tallies for all apps
                    for app in self.tally_apps:
                        app.tally_column(self, column_index)
                
                for app in self.tally_apps:
                    #note/melodic interval tallies for all apps
                    app.tally_pitch(self, line_index, column_index)

                for across_line_index in range(line_index):
                    for app in self.tally_apps:
                        #cross-line tallies (e.g. voice leading) for all lines before this one
                        app.tally_pitch_across_lines(self, line_index, column_index, across_line_index) 

                for across_column_index in range(column_index):
                    for app in self.tally_apps:
                        #cross-column tallies (e.g. overall voice direction)... QUESTION - will this even be useful?
                        app.tally_pitch_across_columns(self, line_index, column_index, across_column_index) 

    # WORTH IT...?
    # def voice_leading_interval(line_index1, line_index2, column_index):
    #     inverval_line1 = cloud[line_index1][column_index] - cloud[line_index1][column_index-1]
    #     inverval_line2 = cloud[line_index2][column_index] - cloud[line_index2][column_index-1]
    #     return interval_line1 - interval_line2 if cloud[line_index1][column_index] > cloud[line_index2][column_index] else interval_line2 - interval_line1

    def column(self, column_index):
        return [line[column_index] for line in self.pitch_lines]

    def tallies_column(self, column_index):
        return [line[column_index] for line in self.tallies]

    def worst_column_index(self):
        column_sums = [sum(self.tallies_column(c)) for c in range(self.num_columns)]
        return column_sums.index(min(column_sums))

    def column_swap2_weighted(self, column_index):
        tallies_column = self.tallies_column(column_index)
        # RESEARCH THIS STATEMENT... HOW DOES IT WORK?
        indeces_sorted = [i[0] for i in sorted(enumerate(tallies_column), key=lambda x:x[1])]
        swap1 = None
        swap2 = None
        # TO DO... document this
        for i in range(self.num_lines):
            if swap1 is not None and random.randrange(0,5) < 3:
                swap2 = indeces_sorted[i]
                self.pitch_lines[swap1][column_index], self.pitch_lines[swap2][column_index] = self.pitch_lines[swap2][column_index], self.pitch_lines[swap1][column_index]
                break
            if random.randrange(0,2) == 0:
                swap1 = indeces_sorted[i]

    def randomize_column(self, column_index):
        # any more efficient way to do this...?        
        # TO DO... DON'T RANDOMIZE dont_touch_pitches
        # a new list for the column
        new_column = [x[column_index] for x in self.pitch_lines]
        # randomize the new column
        random.shuffle(new_column, random.random)
        for i, line in enumerate(self.pitch_lines):
            line[column_index] = new_column[i]

    def randomize_all_columns(self):
        for c in range(self.num_columns):
            self.randomize_column(c)

    def rearrange_try(self):
        try_type_number = random.randrange(0,5)
        if try_type_number == 0:
            # completely randomize the worst column
            self.randomize_column(self.worst_column_index())
        elif try_type_number == 1:
            # swap 2 (weighted) in the worst column
            self.column_swap2_weighted(self.worst_column_index())
        elif try_type_number == 2:
            # swap 2 (weighted) in all columns
            for i in range(self.num_columns):
                self.column_swap2_weighted(i)
        elif try_type_number == 3:
            # completely randomize some random column
            self.randomize_column(random.randrange(self.num_columns))
        elif try_type_number == 4:
            # swap 2 (weighted) in some random column
            self.column_swap2_weighted(random.randrange(self.num_columns))


    def get_rearranged(self):
        tries = []
        best_try = self
        # BETTER TO USE RECURSION HERE?
        # this should get a variety of try type cominations...
        for i in range(3):
            i_try = copy.deepcopy(self)
            i_try.rearrange_try()
            i_try.get_tallies()
            if i_try.tally_total > best_try.tally_total:
                best_try = i_try
            for j in range(3):
                j_try = copy.deepcopy(i_try)
                j_try.rearrange_try()
                j_try.get_tallies()
                if j_try.tally_total > best_try.tally_total:
                    best_try = j_try
                for k in range(3):
                    k_try = copy.deepcopy(j_try)
                    k_try.rearrange_try()
                    k_try.get_tallies()
                    if k_try.tally_total > best_try.tally_total:
                        best_try = k_try
        return best_try


    def save(self, filepath=None):
        if filepath==None:
            filepath = self.filepath
        cloud_data = {}
        cloud_data["pitch_lines"] = self.pitch_lines
        cloud_data["voice_ranges"] = self.voice_ranges
        cloud_data["dont_touch_pitches"] = self.dont_touch_pitches

        with open(filepath, "wb") as p_file:
            pickle.dump(cloud_data, p_file)

    def load(self, filepath=None):
        if filepath==None:
            filepath = self.filepath

        with open(filepath, "rb") as p_file:
            cloud_data = pickle.load(p_file)

        for pickle_attr in cloud_data:
            setattr(self, pickle_attr, cloud_data[pickle_attr])
        self.init_data()

    def show(self):
        arrangement = Arrangement(project=self.project, title="Cloud Pitch Lines: SCORE = " + str(self.tally_total), name="cloud-pitches-show")
        for i, line in enumerate(self.pitch_lines):
            arrangement.add_part(name="line" + str(i), instrument=instrumenttools.Instrument(instrument_name="Line " + str(i), short_instrument_name=str(i)))
            line_music = scoretools.make_notes(line, durationtools.Duration(1,4))
            arrangement.parts["line" + str(i)].extend(line_music)

        # TO DO... remove bar lines (or barlines every note?)
        # TO DO... show scores!

        arrangement.show_pdf()


    def tally_loop(self, times=22, filepath=None):

        k=input("Enter 't' to rearrange and re-tally, 'l' to load, 's' to save, 'p' to show pdf, 'q' to quit: ")

        cloud = self

        if filepath is None:
            filepath = self.filepath

        if k== "t":
            for i in range(times):
                cloud = cloud.get_rearranged()
            print("Tried rearranging " + str(times) + " times...")
            print("New total tally:" + str(cloud.tally_total))
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "l":
            cloud.load(filepath)
            print("Loaded " + filepath)
            cloud.get_tallies()
            print("Total tally:" + str(cloud.tally_total))
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "p":
            cloud.show()
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "s":
            cloud.save(filepath)
            print("Saved!")
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "q":
            # do nothing to quit
            pass

        else:
            print("(invalid entry)")
            cloud = CloudPitches.tally_loop(cloud)

        return cloud

    # TO DO... figure out how to build up a library of these weigting functions... such as:
    # - no parallel pitch classes
    # - no repeated notes
    # - no triple repeated notes
    # - repetitions only allowed at certain positions
    # - minor on bottom
    # - limit voice diatonic spread
    # - small to large interval spread (and vice versa)
    # - voices going up / going down
    # - nice melodic intervals
    # - emphasize repeated notes

