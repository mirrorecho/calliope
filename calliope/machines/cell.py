import calliope

class Cell(calliope.EventMachine):
    print_kwargs = ("rhythm", "pitches")
    child_types = (calliope.EventMachine, ) # TO DO: ???

    def __init__(self, *args, **kwargs):
        self.child_types = child_types = (calliope.Cell, calliope.Event) # just to be safe
        super().__init__(*args, **kwargs)

# TO DO ???
class ContainerCell(Cell):
    """
    By default, an abjad container is only created for the outermost machine... 
    but this ContainerCell is used to create a container for the cell itself...
    """
    def get_signed_ticks_list(self, **kwargs):
        return [self.ticks]

# TO DO ???
class CustomCell(Cell):
    child_types = ()
    set_beats = None
    set_rhythm = () # generally wouldn't be used unless attempting something slick... but needed for base class
    set_pitches = () # ditto
    can_have_children = False
    must_have_children = False
    rest = False
    
    _ticks = 0

    def __init__(self, *args, **kwargs):
        self.beats = kwargs.pop("beats", None) or self.set_beats
        super().__init__(*args, **kwargs)

    def music(self, **kwargs):
        # NOTE... could override this for custom logic, 
        # or simply use music_contents attribute for simple strings
        return calliope.Bubble.music(self, **kwargs)

    @property
    def ticks(self):
        return self._ticks

    @ticks.setter
    def ticks(self, value):
        self._ticks = value

    @property
    def beats(self):
        return int(self._ticks / self.rhythm_default_multiplier)

    @beats.setter
    def beats(self, my_beats):
        if my_beats:
            self._ticks = int(my_beats * self.rhythm_default_multiplier)
            

