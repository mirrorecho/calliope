import abjad
import calliope

class Filter(calliope.Transform):
    args = ()
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if args:
            self.args = args

    def filter_method(self, item):
        return True

    def transform_nodes(self, machine):
        # print( list(filter(lambda c : self.filter_method(c), machine.children)) )
        machine[:] = list(filter(lambda c : self.filter_method(c), machine))
 
    def filter_method(self, item):
        return any( [
            (callable(arg) and arg(item)) or item.my_index == arg or item.name == arg
            for arg in self.args
            ] )

class Remove(Filter):
    def filter_method(self, item):
        # print(super().filter_method(item))
        return not super().filter_method(item)


        
