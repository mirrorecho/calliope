from abjad import *

from calliope.work import Bubble

import os
import random
import copy
import pickle
import tkinter
import time
import threading

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

class TallyRepeatedJumps(TallyAppBase):
    def __init__(self, min_jump=3, over_incremental_multiplier=-2, back_again_multiplier=0.5, line_weights=None, column_weights=None):
        self.min_jump=3
        self.back_again_multiplier = back_again_multiplier # this let's us say that jumps back to the same pitch not as bad
        self.over_incremental_multiplier = over_incremental_multiplier
        super().__init__(line_weights=line_weights, column_weights=column_weights)
    
    def tally_pitch(self, cloud, line_index, column_index):
        if column_index > 0 and column_index < cloud.num_columns-1:
            jump_1 = abs(cloud.pitch_lines[line_index][column_index] - cloud.pitch_lines[line_index][column_index-1])
            jump_2 = abs(cloud.pitch_lines[line_index][column_index] - cloud.pitch_lines[line_index][column_index+1])
            if jump_1 >= self.min_jump and jump_2 >= self.min_jump:
                rating_multiplier = self.over_incremental_multiplier
                if cloud.pitch_lines[line_index][column_index-1] == cloud.pitch_lines[line_index][column_index+1]:
                    rating_multiplier = rating_multiplier * self.back_again_multiplier
                cloud.add_tally(line_index, column_index, (jump_1+jump_2)*self.over_incremental_multiplier)


class TallyMelodicIntervals(TallyAppBase):
    def __init__(self, interval_ratings=[], over_incremental_multiplier=None, by_pitch_class=False, bidirectional=True, line_weights=None, column_weights=None, down_rating=0, up_rating=0):
        self.interval_ratings = interval_ratings
        self.by_pitch_class = by_pitch_class
        self.bidirectional = bidirectional
        self.over_incremental_multiplier = over_incremental_multiplier
        self.up_rating=up_rating
        self.down_rating=down_rating
        super().__init__(line_weights=line_weights, column_weights=column_weights)

    def tally_pitch(self, cloud, line_index, column_index):
        # only makes sense starting from 2nd column:
        if column_index > 0:
            melodic_interval = cloud.pitch_lines[line_index][column_index] - cloud.pitch_lines[line_index][column_index-1]
            
            if self.up_rating and melodic_interval:
                cloud.add_tally(line_index, column_index, self.up_rating)
            if self.down_rating and melodic_interval:
                cloud.add_tally(line_index, column_index, self.down_rating)

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

    def __init__(self, pitch_lines=None, pitch_ranges=None, filename=None, project=None, autoload=False):
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
        
        self.pitch_ranges = pitch_ranges # TO DO... extrapolate last entry for total # of lines/columns
        if self.pitch_ranges is not None:
            self.auto_move_into_ranges = True
        else:
            self.auto_move_into_ranges = False

        if pitch_lines is not None:
            self.pitch_lines = pitch_lines
        elif autoload and os.path.isfile(self.filepath):
            self.load()
        else:
            self.pitch_lines = [[]]

        self.init_data()

        self.tally_apps = []

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

    def second_worst_column_index(self):
        column_sums = [sum(self.tallies_column(c)) for c in range(self.num_columns)]
        worst_index = column_sums.index(min(column_sums))
        column_sums[worst_index] = abs(self.tally_total) + 1 # pretend the worst column is better than all columns combined
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

    def column_swap2(self, column_index):
        swap1 = random.randrange(self.num_lines)
        swap2 = swap1
        while swap2 != swap1:
            swap2 = random.randrange(self.num_lines)
        self.pitch_lines[swap1][column_index], self.pitch_lines[swap2][column_index] = self.pitch_lines[swap2][column_index], self.pitch_lines[swap1][column_index]

    def move_into_ranges(self):
        if self.pitch_ranges is not None:
            for l in range(self.num_lines):
                range_line = self.pitch_ranges[l % len(self.pitch_ranges)]
                for c in range(self.num_columns):
                    self.pitch_lines[l][c] = pitchtools.transpose_pitch_expr_into_pitch_range([self.pitch_lines[l][c]], range_line[c % len(range_line)])[0]
        else:
            print("Tried moving pitches into ranges, but pitch_ranges is None")

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

    # one thought could be to swap 2 in columns before/after worst or 2nd worst column...
    def rearrange_try(self, depth):
        try_type_number = random.randrange(0+depth,8+depth)
        # these are roughly ordered from most eratic/dramatic to most direct... at a lower depth, the
        # more eratic/dramatic ones will be attempted...
        if try_type_number == 0:
            # completely randomize some random column and swap 2 in worst and 2nd worst columns (not weighed)
            self.randomize_column(random.randrange(self.num_columns))
            self.column_swap2(self.worst_column_index())
            self.column_swap2(self.second_worst_column_index())
        elif try_type_number == 1:
            # completely randomize the second worst column and swap 2 in worst column
            self.randomize_column(self.second_worst_column_index())
            self.column_swap2(self.worst_column_index())
        elif try_type_number == 2:
            # completely randomize the worst column and swap 2 in 2nd worst column
            self.randomize_column(self.worst_column_index())
            self.column_swap2(self.second_worst_column_index())
        elif try_type_number == 3:
            # swap 2 (weighted) in all columns
            for i in range(self.num_columns):
                self.column_swap2_weighted(i)        
        elif try_type_number == 4:
            # swap 2 (weighted) in some random column  ... and swap 2 (not weighted) in worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2_weighted(random.randrange(self.num_columns))
            self.column_swap2(self.worst_column_index())
        elif try_type_number == 5 or try_type_number:          
            # swap 2 (weighted) in only the second worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2_weighted(self.second_worst_column_index())
        elif try_type_number == 6 or try_type_number == 11:
            # swap 2 (weighted) in the worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2_weighted(self.worst_column_index())
        elif try_type_number == 7:
            # swap 2 (not weighted) in worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2(self.worst_column_index())
        elif try_type_number == 8:
            # swap 2 (weighted) in some random column 
            self.column_swap2_weighted(random.randrange(self.num_columns))
        elif try_type_number == 9:
            # swap 2 (weighted) in the worst column... twice
            self.column_swap2_weighted(self.worst_column_index())
            self.column_swap2_weighted(self.worst_column_index())
        elif try_type_number == 10:
            # swap 2 (weighted) in the worst and second worst columns
            self.column_swap2_weighted(self.worst_column_index())
            self.column_swap2_weighted(self.second_worst_column_index())

        if self.auto_move_into_ranges:
            
            #passable way to move pitches into matching octave
            for l in range(self.num_lines):
                for c in range(self.num_columns):
                    if c == 0:
                        if (self.pitch_lines[l][c+1] - self.pitch_lines[l][c]) < -6 and random.randrange(2) == 1:
                            self.pitch_lines[l][c] -= 12
                        elif (self.pitch_lines[l][c+1] - self.pitch_lines[l][c]) > 6 and random.randrange(2) == 1:
                            self.pitch_lines[l][c] += 12
                    elif c == self.num_columns-1:
                        if (self.pitch_lines[l][c-1] - self.pitch_lines[l][c]) < -6 and random.randrange(2) == 1:
                            self.pitch_lines[l][c] -= 12
                        elif (self.pitch_lines[l][c-1] - self.pitch_lines[l][c]) > 6 and random.randrange(2) == 1:
                            self.pitch_lines[l][c] += 12
                    else:
                        if (self.pitch_lines[l][c+1] + self.pitch_lines[l][c-1]) - (self.pitch_lines[l][c] * 2) < -12 and random.randrange(2) == 1:
                            self.pitch_lines[l][c] -= 12
                        elif (self.pitch_lines[l][c+1] + self.pitch_lines[l][c-1]) - (self.pitch_lines[l][c] * 2) > 12 and random.randrange(2) == 1:
                            self.pitch_lines[l][c] += 12

            self.move_into_ranges()


    def get_rearranged(self):
        tries = []
        best_try = self
        # BETTER TO USE RECURSION HERE?
        # this should get a variety of try type combinations...
        for i in range(2):
            i_try = copy.deepcopy(self)
            i_try.rearrange_try(0)
            i_try.get_tallies()
            if i_try.tally_total > best_try.tally_total:
                best_try = i_try
            for j in range(2):
                j_try = copy.deepcopy(i_try)
                j_try.rearrange_try(1)
                j_try.get_tallies()
                if j_try.tally_total > best_try.tally_total:
                    best_try = j_try
                for k in range(2):
                    k_try = copy.deepcopy(j_try)
                    k_try.rearrange_try(2)
                    k_try.get_tallies()
                    if k_try.tally_total > best_try.tally_total:
                        best_try = k_try
                    for l in range(2):
                        l_try = copy.deepcopy(k_try)
                        l_try.rearrange_try(3)
                        l_try.get_tallies()
                        if l_try.tally_total > best_try.tally_total:
                            best_try = l_try
                        for m in range(2):
                            m_try = copy.deepcopy(l_try)
                            m_try.rearrange_try(4)
                            m_try.get_tallies()
                            if m_try.tally_total > best_try.tally_total:
                                best_try = m_try
        if best_try is not self:
            self.pitch_lines = best_try.pitch_lines
            self.tallies = best_try.tallies
            self.tally_total = best_try.tally_total



    def save(self, filepath=None):
        if filepath==None:
            filepath = self.filepath
        cloud_data = {}
        cloud_data["pitch_lines"] = self.pitch_lines
        cloud_data["pitch_ranges"] = self.pitch_ranges
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

        print("Loaded cloud pitch data from " + filepath)

    def show(self):
        bubble = Bubble(project=self.project, title="Cloud Pitch Lines: SCORE = " + str(self.tally_total), name="cloud-pitches-show")
        for i, line in enumerate(self.pitch_lines):
            bubble.add_part(name="line" + str(i), instrument=instrumenttools.Instrument(instrument_name="Line " + str(i), short_instrument_name=str(i)))
            line_music = scoretools.make_notes(line, durationtools.Duration(1,4))
            bubble.parts["line" + str(i)].extend(line_music)

        # TO DO... remove bar lines (or barlines every note?)
        # TO DO... show scores!

        bubble.show_pdf()


    def tally_loop(self, times=9, filepath=None):

        # see http://stackoverflow.com/questions/11758555/python-do-something-until-keypress-or-timeout
        # for more on how this threading works...
        cloud = self

        def re_tally():
            T0 = time.clock()
            while not stop_event.isSet(): #as long as long as flag is not set 
                cloud.get_rearranged() # WTF, why doesn't cloud = cloud.get_rearranged() work???
                print("Total tally:" + str(cloud.tally_total))
                time.sleep(0.1)

        def _stop_tally():
            print("Stopping tally after this try...")
            stop_event.set()
            thread.join() #wait for the thread to finish
            root.quit()
            root.destroy()

        if filepath is None:
            filepath = self.filepath

        k=input("Enter 't' start re-tallying, 'l' to load, 'r' to re-randomize, 's' to save, 'p' to show pdf, 'q' to quit: ")

        if k== "t":
            
            root = tkinter.Tk()
            quit_button = tkinter.Button(master=root, text='Stop re-tallying', command=_stop_tally) #the quit button
            quit_button.pack(side=tkinter.BOTTOM)
            thread = threading.Thread(target=re_tally, args=())
            stop_event = threading.Event()
            thread.start()
            root.mainloop()
            
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "l":
            cloud.load(filepath)
            print("Loaded " + filepath)
            cloud.get_tallies()
            print("Total tally:" + str(cloud.tally_total))
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "r":
            cloud.randomize_all_columns()
            cloud.get_tallies()
            print("Randomized all columns... new tally is: " + str(cloud.tally_total))
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "p":
            cloud.show()
            cloud = CloudPitches.tally_loop(cloud)

        elif k == "s":
            cloud.save(filepath)
            print("Saved to " + filepath + "!")
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

