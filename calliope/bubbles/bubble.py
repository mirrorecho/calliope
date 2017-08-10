import inspect
import abjad
from calliope import tools, structures, bubbles


class Bubble(structures.Tree):
    container_type=abjad.Container
    context_name=None
    respell=None # TO DO, best place for this?
    stylesheets = () # TO DO, best place for this?
    is_simultaneous=True
    # NOTE: should never set "name" attribute at the class level... because it's an attribute (with setter logic) on the abjad TreeContainer

    def _init_make_callable(self, attr_name):
        attr = getattr(self, attr_name, None)
        if attr is not None:
            if isinstance(attr, Bubble):
                setattr(self, attr_name, attr.blow)
            elif callable(attr):
                setattr(self, attr_name, attr)
            else:
                setattr(self, attr_name, lambda : attr)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.child_types:
            self.child_types = (Bubble,)
        self._init_make_callable("music")
        self._init_make_callable("sequence")

    def map_to(self, *args, **kwargs):
        # TO DO... IMPLEMENT MORE FULLY
        bubble_type = args[0]
        if type(args[1]) is bubbles.Mapping:
            my_mapping = args[1]
        return bubble_type( *my_mapping.map_root.map_bubble(self, as_copy=True) )

    def map_filter(self, *args, **kwargs):
        if args[0] is Mapping:
            my_mapping = args[0]

    @classmethod
    def isbubble(cls, bubble, bubble_types=None):
        bubble_types = bubble_types or (cls,)
        if isinstance(bubble, bubble_types) or ( inspect.isclass(bubble) and issubclass(bubble, bubble_types) ):
            return True
        return False

    def music_container(self, **kwargs):
        if self.is_simultaneous is not None:
            kwargs["is_simultaneous"] = self.is_simultaneous
        if self.context_name is not None:
            kwargs["context_name"] = self.context_name
        return self.container_type(name=self.name, **kwargs)

    # TO DO... this implementation of add/mul creates odd nested containers... rethink
    # Could also conflict with abjad tree structures
    def __add__(self, other):
        return bubbles.BubbleSequence( sequenced_bubbles=(self, other) )

    def __mul__(self, num):
        return bubbles.BubbleSequence( sequenced_bubbles = [self for i in range(num)] )

    @property
    def ly(self):
        music = self.blow()
        return(format(music))

    def get_lilypond_file(self):
        music = self.blow()
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(music, includes=self.stylesheets, 
            )
        self.info("got abjad representation of lilypond file... now rendering with lilypond")
        return lilypond_file

    def child_music(self, child_bubble):
        # can be overridden to add custom stuff for each child of a particular bubble
        return child_bubble.blow()

    def process_music(self, music, **kwargs):
        # TO DO... is this the best place for respell, etc.?
        if self.respell:
            tools.respell(music, self.respell)

    def music(self, **kwargs):
        my_music = self.music_container()
        for child_bubble in self.children:
            my_music.append( self.child_music( child_bubble ) )
        return my_music

    def blow(self, **kwargs):
        my_music = self.music(**kwargs)
        self.process_music(my_music, **kwargs)
        return my_music

