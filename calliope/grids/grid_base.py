import numpy as np
import pandas as pd
import abjad
import calliope

class GridBase(object):
    def __init__(self, data=None, filepath=None, autoload=False):
        self.data = data or pd.DataFrame()
        self.tallies = pd.DataFrame()
        self.tally_total = 0 # TO DO: consider: simply sum up every time?

        self.filepath = filepath # or ...? what if filepath is None... make up a default?
        # calling_info = inspect.stack()[1]
        # calling_module_path = calling_info[1]

        if autoload:
            self.load()

        self.init_data()

        self.tally_apps = []

    # TO DO.. necessary? remove?
    def init_data(self, data=None):
        if data:
            self.data = data
        self.reset_tally()

    def reset_tally(self):
        """sets tallies dataframe to all zeroes, with same shape as data dataframe"""
        self.tallies = pd.DataFrame(np.zeros(self.data.shape))

    def add_tally(self, column_index, row_index, value):
        self.tallies[column_index][row_index] += value
        self.tally_total += value 

    def add_tally_app(self, tally_app):
        self.tally_apps.append(tally_app)

    def tally_me(self):
        self.reset_tally()
        for column_index in self.data.columns:
            # column tallies for all apps
            for app in self.tally_apps:
                app.tally_column(self, column_index)
            
            for row_index in self.data.rows:    
                
                if column_index == 0:
                    #column tallies for all apps
                    for app in self.tally_apps:
                        app.tally_row(self, row_index)
                
                for app in self.tally_apps:
                    #note/melodic interval tallies for all apps
                    app.tally_item(self, row_index, column_index)

                for across_row_index in range(row_index):
                    for app in self.tally_apps:
                        #cross-line tallies (e.g. voice leading) for all lines before this one
                        app.tally_pitch_across_lines(self, row_index, column_index, across_row_index) 

                for across_column_index in range(column_index):
                    for app in self.tally_apps:
                        #cross-column tallies (e.g. overall voice direction)... QUESTION - will this even be useful?
                        app.tally_pitch_across_columns(self, row_index, column_index, across_column_index) 

    @property
    def is_loaded(self):
        return self.data.shape[0] > 0 and self.data.shape[1] > 0
