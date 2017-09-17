import random
import copy
import tkinter
import time
import threading
import types
import numpy as np
import pandas as pd

import abjad
import calliope

class GridBase(calliope.CalliopeBaseMixin):
    to_bubble_type = calliope.Bubble
    row_to_bubble_type = calliope.Fragment
    output_directory = None
    save_attrs = ("data", "start_data")
    version = 1

    tally_total = 0

    data = None # to be set to instance of a DataFrame
    start_data = None

    tallies = None # to be set to instance of a DataFrame
    auto_load = True
    name = None

    def __init__(self, *args, **kwargs):
        if "get_start_data" in kwargs:
            self.get_start_data = types.MethodType( kwargs.pop("get_start_data"), self )

        self.setup(**kwargs)
        self.tally_apps = list(args)

        if self.auto_load:
            self.load()

        self.init_data()

    def get_start_data(self):
        return pd.DataFrame()

    # TO DO.. necessary? remove?
    def init_data(self, start_data=None, data=None, reset=False):
        if start_data is None:
            start_data = self.get_start_data()
            start_data.name = self.name        
        if reset or self.start_data is None or self.data is None:
            self.start_data = start_data
            if data is None:
                data = start_data.copy()   
            self.data = data
        elif not self.start_data.equals(start_data):
            self.warn(
                "loaded start data does not match new start data... consider resetting the data"
                )
            self.info("loaded start data", self.start_data)
            self.info("new start data", start_data)

        self.reset_tally()

    @classmethod
    def from_bubble(cls, bubble, *args, **kwargs):
        bubble_records = [cls.row_list_from_bubble(b) for b in bubble]
        kwargs["output_directory"] = bubble.get_module_info()[0]
        kwargs["get_start_data"] = lambda s: pd.DataFrame.from_records(bubble_records)
        kwargs["name"] = "from_%s" % (bubble.name or bubble.__class__.__name__)
        return cls(*args, **kwargs)

    @classmethod
    def row_list_from_bubble(self, bubble):
        return [cls.item_from_bubble(b) for b in bubble]

    @classmethod
    def item_from_bubble(self, bubble):
        return bubble

    def illustrate_me(self):
        self.to_bubble().illustrate_me(directory=self.output_directory)

    def illustrate_start(self):
        show_copy = self.copy_me(reset=True)
        show_copy.name += "_start"
        show_copy.illustrate_me()

    def to_bubble(self, bubble_type=None, row_bubble_type=None):
        return (bubble_type or self.to_bubble_type)(
            *self.data.apply(lambda row: self.row_to_bubble(row, row_bubble_type), axis=1),
            name = "%s_%s" % (self.name, self.__class__.__name__)
            )

    def row_to_bubble(self, row, row_bubble_type=None):
        return (row_bubble_type or self.row_to_bubble_type)(
            *row.apply(self.item_to_bubble)
            )

    def item_to_bubble(self, item):
        return item

    def get_output_file_path(self, save_attr):
        return self.get_output_path(
            directory=self.output_directory, 
            sub_directory = "data",
            filename_suffix = "%s.%s" % (save_attr, self.version) 
            ) + ".json"

    def save(self, **kwargs):
        for save_attr in self.save_attrs:
            attr = getattr(self, save_attr, None)
            if attr is not None:
                file_path = self.get_output_file_path(save_attr)
                # TO DO: consider using python's json to format the json file to be readable
                attr.to_json(file_path, orient="split")
                self.info("saved " + file_path)

    def load(self, **kwargs):
        for save_attr in self.save_attrs:
            file_path = self.get_output_file_path(save_attr)
            try:
                setattr(self, save_attr, pd.read_json(file_path, orient="split"))
            except:
                self.warn("cannot read json file " + file_path)

    def copy_me(self, reset=False):
        my_copy = copy.copy(self)
        data = self.start_data.copy() if reset else self.data.copy()
        my_copy.init_data(start_data=self.start_data, data=data, reset=True)
        return my_copy

    def reset_tally(self):
        """sets tallies dataframe to all zeroes, with same shape as data dataframe"""
        self.tallies = pd.DataFrame(np.zeros(self.data.shape))
        self.tally_total = 0

    def add_tally(self, r, c, value):
        self.tallies.iat[r, c] += value
        self.tally_total += value 

    def add_tally_apps(self, *args):
        self.tally_apps.extend(args)

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
                r_swap2 = indices_sorted[r]
                self.data.iat[r_swap1, c], self.data.iat[r_swap2, c] = self.data.iat[r_swap2, c], self.data.iat[r_swap1, c]
                break
            if random.randrange(0,2) == 0:
                r_swap1 = indices_sorted[r]

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
        # these are roughly ordered from most eratic/dramatic to simplest... at a lower depth, the
        # more eratic/dramatic ones will be attempted...
        sorted_column_indices = self.column_indices_by_tally()
        if try_type_number == 0:
            # completely randomize some random column and swap 2 in worst and 2nd worst columns (not weighed)
            self.randomize_column(random.randrange(self.data.shape[1]))
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
        # print(best_copy.tally_total, my_copy.tally_total)
        if my_copy.tally_total > best_copy.tally_total:
            best_copy = my_copy
        if depth_counter < depth:
            return my_copy.get_rearranged(best_copy, depth, depth_counter+1)
        else:
            return best_copy

    def rearrange_me(self):
        best_copy = self.get_rearranged()
        if best_copy is not self:
            # print("YO BETTER")
            self.data = best_copy.data
            self.tallies = best_copy.tallies # TO DO: even necessary?
            self.tally_total = best_copy.tally_total

    def tally_loop(self, times=9):

        # see http://stackoverflow.com/questions/11758555/python-do-something-until-keypress-or-timeout
        # for more on how this threading works...
        # cloud = self
        # cloud_type = type(self)
        self.tally_me()

        def re_tally():
            T0 = time.clock()
            while not stop_event.isSet(): #as long as long as flag is not set 
                self.rearrange_me() 
                # self.pitch_lines = best_try.pitch_lines
                # self.tallies = best_try.tallies
                # self.tally_total = best_try.tally_total
                self.info("total tally:" + str(self.tally_total))
                time.sleep(0.1)

        def _stop_tally():
            self.info("stopping tally after this try...")
            stop_event.set()
            thread.join() #wait for the thread to finish
            root.quit()
            root.destroy()

        k=input("""
    ENTER:
        't' start re-tallying, 
        'v' to change version,
        'l' to (re)load from file, 
        'd' to reset data (getting start data again),
        'r' to re-randomize, 
        's' to save, 
        'p' to show pdf, 
        'o' to show pdf of original start data, 
        '/' to show data output path, 
        'q' to quit
    """)

        if k == "t":
            
            root = tkinter.Tk()
            quit_button = tkinter.Button(master=root, text='Stop re-tallying', command=_stop_tally) #the quit button
            quit_button.pack(side=tkinter.BOTTOM)
            thread = threading.Thread(target=re_tally, args=())
            stop_event = threading.Event()
            thread.start()
            root.mainloop()
            self.tally_loop(times)

        elif k == "v":
            kv = input("Enter version #:")
            self.version = int(kv)
            self.into("set version to %s" % kv)
            self.tally_loop(times)

        elif k == "l":
            self.load()
            # print("Loaded ")
            self.tally_me()
            self.info("total tally:" + str(self.tally_total))
            self.tally_loop(times)

        elif k == "d":
            self.init_data(reset=True)
            self.tally_loop(times)

        elif k == "r":
            self.randomize_all_columns()
            self.tally_me()
            self.info("randomized all columns... new tally is: " + str(self.tally_total))
            self.tally_loop(times)

        elif k == "s":
            self.save()
            self.tally_loop(times)

        elif k == "p":
            self.illustrate_me()
            self.tally_loop(times)

        elif k == "o":
            self.illustrate_start()
            self.tally_loop(times)

        elif k == r"/":
            self.info(self.get_output_file_path("[data_attr]"))
            self.tally_loop(times)

        elif k == "q":
            # do nothing to quit
            pass

        else:
            self.warn("(invalid entry)")
            self.tally_loop(times)

    @property
    def range_rows(self):
        return range(self.data.shape[0])

    @property
    def range_cols(self):
        return range(self.data.shape[1])

    @property
    def is_loaded(self):
        return self.data.shape[0] > 0 and self.data.shape[1] > 0
