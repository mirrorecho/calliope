import numpy as np
import pandas as pd
import abjad
import calliope

class GridBase(calliope.CalliopeBaseMixin):
    to_bubble_type = calliope.Bubble
    row_to_bubble_type = calliope.Fragment
    output_path = ""
    tally_total = 0

    data = None # to be set to instance of a DataFrame
    tallies = None # to be set to instance of a DataFrame
    auto_load = True
    name = None

    def __init__(self, *args, **kwargs):
        self.setup(**kwargs)
        self.save_attrs = ["data"]
        self.tally_apps = []

        if self.auto_load:
            self.load()

        self.init_data()

    # TO DO.. necessary? remove?
    def init_data(self, data=None):
        if data:
            self.data = data
        if self.data is None:
            self.data = pd.DataFrame()
        self.data.name = self.name
        self.reset_tally()

    @classmethod
    def from_bubble(cls, bubble, **kwargs):
        bubble_records = [ [cls.item_from_bubble(r) for r in c] for c in bubble]
        kwargs["output_path"] = bubble.get_output_path(sub_directory="data")
        return cls(data=pd.DataFrame.from_records(bubble_records), **kwargs)

    @classmethod
    def item_from_bubble(self, bubble):
        return bubble


    def to_bubble(self, bubble_type=None, row_bubble_type=None):
        return (bubble_type or self.to_bubble_type)(
            *self.data.apply(lambda row: self.row_to_bubble(row, row_bubble_type), axis=1)
            )

    def row_to_bubble(self, row, row_bubble_type=None):
        return (row_bubble_type or self.row_to_bubble_type)(
            *row.apply(self.item_to_bubble)
            )

    def item_to_bubble(self, item):
        return item


    def copy_me(self):
        my_copy = copy.copy(self)
        my_copy.init_data(data=self.data.copy())
        return my_copy

    def reset_tally(self):
        """sets tallies dataframe to all zeroes, with same shape as data dataframe"""
        self.tallies = pd.DataFrame(np.zeros(self.data.shape))

    def add_tally(self, r, c, value):
        self.tallies.iat[r, c] += value
        self.tally_total += value 

    def add_tally_app(self, tally_app):
        self.tally_apps.append(tally_app)

    def tally_me(self):
        self.reset_tally()
        # TO DO: eventually... this could probably be made much cleaner with pandas apply methods

        for r in self.range_rows:   
            #column tallies for all apps
            for app in self.tally_apps:
                app.tally_row(self, r)

            for c in self.range_cols:
                # column tallies for all apps
                if c == 0:
                    for app in self.tally_apps:
                        app.tally_column(self, c)
               
                for app in self.tally_apps:
                    #note/melodic interval tallies for all apps
                    app.tally_item(self, r, c)

                for across_r in range(r):
                    for app in self.tally_apps:
                        #cross-line tallies (e.g. voice leading) for all lines before this one
                        app.tally_item_across_rows(self, r, c, across_r) 

                for across_c in range(c):
                    for app in self.tally_apps:
                        #cross-column tallies (e.g. overall voice direction)... QUESTION - will this even be useful?
                        app.tally_item_across_columns(self, r, c, across_c) 

    def column_indices_by_tally(self):
        return self.tallies.sum().sort_values().index

    def column_swap2_weighted(self, c):
        indices_sorted = self.tallies[c].sort_values().index
        r_swap1, r_swap2 = None, None
        for r in self.range_rows:
            if r_swap1 and random.randrange(0,5) < 3:
                r_swap2 = indices_sorted.iat[r]
                self.data.iat[r_swap1, c], self.data.iat[r_swap2, c] = self.data.iat[r_swap2, c], self.data.iat[r_swap1, c]
                break
            if random.randrange(0,2) == 0:
                r_swap1 = indices_sorted.iat[r]

    def column_swap2(self, c):
        r_swap1, r_swap2 = None, None
        while r_swap1 == r_swap2:
            r_swap1, r_swap2 = random.choice(self.range_rows), random.choice(self.range_rows)
        self.data.iat[r_swap1, c], self.data.iat[r_swap2, c] = self.data.iat[r_swap2, c], self.data.iat[r_swap1, c]

    def randomize_column(self, c):
        np.random.shuffle(self.data[c])

    def randomize_all_columns(self):
        for c in self.range_cols:
            self.randomize_column(c)

    # one thought could be to swap 2 in columns before/after worst or 2nd worst column...
    def rearrange_try(self, depth):
        try_type_number = random.randrange(0+depth,8+depth)
        # these are roughly ordered from most eratic/dramatic to most direct... at a lower depth, the
        # more eratic/dramatic ones will be attempted...
        sorted_column_indices = self.column_indices_by_tally()
        if try_type_number == 0:
            # completely randomize some random column and swap 2 in worst and 2nd worst columns (not weighed)
            self.randomize_column(random.randrange(self.num_columns))
            self.column_swap2(sorted_column_indices[0])
            self.column_swap2(sorted_column_indices[1])
        elif try_type_number == 1:
            # completely randomize the second worst column and swap 2 in worst column
            self.randomize_column(sorted_column_indices[1])
            self.column_swap2(sorted_column_indices[0])
        elif try_type_number == 2:
            # completely randomize the worst column and swap 2 in 2nd worst column
            self.randomize_column(sorted_column_indices[0])
            self.column_swap2(sorted_column_indices[1])
        elif try_type_number == 3:
            # swap 2 (weighted) in all columns
            for c in self.data.columns:
                self.column_swap2_weighted(c)        
        elif try_type_number == 4:
            # swap 2 (weighted) in some random column  ... and swap 2 (not weighted) in worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2_weighted(random.choice(self.data.columns))
            self.column_swap2(sorted_column_indices[0])
        elif try_type_number == 5 or try_type_number:          
            # swap 2 (weighted) in only the second worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2_weighted(sorted_column_indices[1])
        elif try_type_number == 6 or try_type_number == 11:
            # swap 2 (weighted) in the worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2_weighted(sorted_column_indices[0])
        elif try_type_number == 7:
            # swap 2 (not weighted) in worst column
            # (this option is ALWAYS a possibility)
            self.column_swap2(sorted_column_indices[0])
        elif try_type_number == 8:
            # swap 2 (weighted) in some random column 
            self.column_swap2_weighted(random.choice(self.data.columns))
        elif try_type_number == 9:
            # swap 2 (weighted) in the worst column... twice
            self.column_swap2_weighted(sorted_column_indices[0])
            self.column_swap2_weighted(sorted_column_indices[0])
        elif try_type_number == 10:
            # swap 2 (weighted) in the worst and second worst columns
            self.column_swap2_weighted(sorted_column_indices[0])
            self.column_swap2_weighted(sorted_column_indices[1])

    def get_rearranged(self, 
            best_copy=None, 
            depth=9, # TO DO: consider... where best to set this default?
            depth_counter=0,
            ):
        best_copy = best_copy or self
        my_copy = self.copy_me()
        my_copy.rearrange_try(depth_counter)
        my_copy.tally_me()
        if my_copy.tally_total > best_copy.tally_total:
            best_copy = my_copy
        if depth_counter < depth:
            return my_copy.get_rearranged(best_copy, depth, depth_counter+1)
        else:
            return best_copy

    def rearrange_me(self):
        best_copy = self.get_rearranged()
        if best_copy is not self:
            self.data = best_copy.data
            self.tallies = best_copy.tallies # TO DO: even necessary?
            self.tally_total = best_copy.tally_total

    def save(self, output_path=None):
        for save_attr in self.save_attrs:
            attr = getattr(self, save_attr, None)
            if attr:
                file_path = (output_path or self.output_path) + "_" + save_attr + ".json"
                attr.to_json(file_path, orient="records", lines=True)

    def load(self, output_path=None):
        for save_attr in self.save_attrs:
            file_path = (output_path or self.output_path) + "_" + save_attr + ".json"
            try:
                setattr(self, save_attr, pd.read_json(file_path, orient="records", lines=True))
            except:
                print("ERROR READING JSON FILE: " + file_path)



    def tally_loop(self, times=9, filepath=None):

        # see http://stackoverflow.com/questions/11758555/python-do-something-until-keypress-or-timeout
        # for more on how this threading works...
        cloud = self

        def re_tally():
            T0 = time.clock()
            while not stop_event.isSet(): #as long as long as flag is not set 
                cloud.get_rearranged() 
                self.pitch_lines = best_try.pitch_lines
                self.tallies = best_try.tallies
                self.tally_total = best_try.tally_total
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
            cloud.to_bubble().illustrate_me()
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

    @property
    def range_rows(self):
        return range(self.data.shape[0])

    @property
    def range_cols(self):
        return range(self.data.shape[1])

    @property
    def is_loaded(self):
        return self.data.shape[0] > 0 and self.data.shape[1] > 0