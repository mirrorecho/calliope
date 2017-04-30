from calliope import machines

class Machine(bubbles.LineTalea):
    """
    Base class .... creates music out of defined segments of material in the data attribute 
    (a tree structure of data about phrases, cells, events and logical ties).
    
    Plural  set_ methods are overriden in mixins to create/update various levels of data.
    
    In general, these plural methods are called only called once for object they are adding items to... calling them multiple times for the same 
    object could produce unintended results (e.g. doubly adding something). 
    
    Singular set_ methods set the attribues on indiviaul objects, usually based on data elsewhere in the data structure, or defined at the class
    level.
    """
    data = None

    def __init__(self, **kwargs):
        self.data = machines.MachineData()
        self.set_phrases(**kwargs)
        self.cleanup_data(**kwargs)
        self.update_data(**kwargs)
        super().__init__(**kwargs) # note arrange() is called by BubbleBase __init__ method

    @property
    def segments(self):
        return self.data.children

    @property
    def events(self):
        return self.data.events

    @property
    def logical_ties(self):
        return self.data.leaves

    def set_leaf(self, leaf, **kwargs):
        pass

    def set_leaves(self, logical_tie, **kwargs):
        pass

    def set_logical_tie(self, logical_tie, **kwargs):
        pass

    def set_logical_ties(self, event, **kwargs):
        pass

    def set_event(self, event, **kwargs):
        pass

    def set_events(self, cell, **kwargs):
        pass

    def set_cell(self, cell, **kwargs):
        pass

    def set_cells(self, phrase, **kwargs):
        pass

    def set_phrase(self, phrase, **kwargs):
        pass

    def set_phrases(self, **kwargs):
        pass

    def update_data(self, **kwargs):
        pass

    def music_from_segments(self, **kwargs):
        pass

    def process_logical_tie(self, music, music_logical_tie, data_logical_tie, music_leaf_count, **kwargs):
        pass

    def process_logical_ties(self, music, **kwargs):
        pass

    def cleanup_data(self, **kwargs):
        pass

    def process_music(self, music, **kwargs):
        pass