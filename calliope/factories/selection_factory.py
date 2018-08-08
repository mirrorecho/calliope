import calliope

class SelectionFactoryMixin(object):
    machine_type = calliope.Cell
    selection = None # to be set to an instance of a selection
    flatten = False
    chord_indices = ()
    root_node = None

    def make(self, **kwargs):
        return self.machine_type
