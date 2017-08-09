import pandas as pd
import numpy as np
import abjad

# TO DO... ever used?
class Series():
    """
    A wrapper around a pandas Series with a few goodies useful for musical structures 
    ?(like cyclic indexing).
    """
    cyclic = False
    cyclic_start = 0
    default = None
    min_limit = 0
    limit = 0

    def __init__(self, *args, **kwargs):
        self._series = pd.Series(*args, **kwargs)

    def __getitem__(self, key):
        # TO DO... implement cyclic slicing?
        if isinstance(key, slice):
            pass
        else:
            if self.default and key not in self._series:
                return self.get_default()
            else:
                return self._series.loc[key]

            # return self._series.get(key, self.default)

    def __iter__(self):
        for x in range(self.min_limit, self.limit):
            yield self[x]

    def __str__(self):
        my_string = str(self._series) + "\n"
        my_string += "default: " + str(self.get_default())
        return my_string

    def get_default(self):
        if hasattr(self.default, "__call__"):
            return self.default()
        else:
            return self.default


    # TO CONSIDER IMPLEMENTING:

    # pandas.Series.update (most likely yes)
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.update.html#pandas.Series.update
    # - will need to reconcile with slightly different IndexedData.update implementation

    # pandas.Series.shift
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.shift.html

    # something with pandas dtype, or IndexedData.item/items_type


# CONSIER:
# class CyclicSeries() # subclass to implement cyclic indexing as opposed to 

# -----------------------------------------------------------------------

class SeriesCollection(abjad.datastructuretools.TypedOrderedDict):

    def __init__(self, items=None):
        super().__init__(items=items, item_class=Series)


# TO CONSIDER... useful?
# class DataFrame:
#     def __init__(self, *args, **kwargs):
#         self._frame = pd.DataFrame(*args, **kwargs)

#     def __str__(self):
#         return str(self._frame.T)
