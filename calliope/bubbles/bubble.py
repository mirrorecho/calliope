import inspect, collections
import abjad
from calliope import tools, bubbles


# TO DO MAYBE: all bubbles inherit from tree structure????
class Bubble(abjad.datastructuretools.TreeContainer):
    container_type=abjad.Container
    context_name=None
    is_simultaneous=False
    child_types = ()
    respell=None # TO DO, best place for this?
    process_methods = () # TO DO... depreciate?
    stylesheets = () # TO DO, best place for this?
    is_simultaneous=True
    # NOTE: should never set "name" attribute at the class level... because it's an attribute (with setter logic) on the abjad TreeContainer

    # sometimes items are moved arround... this can be used track where an element had been placed previously, which is often useful
    original_index = None 
    original_depthwise_index = None # TO DO... consider making these IndexedData objects at the parent level?

    def _init_make_callable(self, attr_name):
        attr = getattr(self, attr_name, None)
        if attr is not None:
            if isinstance(attr, Bubble):
                setattr(self, attr_name, attr.blow)
            # elif isinstance(attr, Material):
            #     setattr(self, attr_name, attr.get)
            elif callable(attr):
                setattr(self, attr_name, attr)
            else:
                setattr(self, attr_name, lambda : attr)

    def _init_append_children(self):
        for bubble_name in type(self).class_sequence():
            # TO DO: WARNING: this won't work for class-based bubbles... implement for classes?
            bubble = getattr(self, bubble_name)
            bubble.name = bubble_name     
            self[bubble_name] = bubble

    def __init__(self, *args, **kwargs):
        children = args
        super().__init__(children)
        name = kwargs.pop("name", None)
        if name:
            self.name = name
        if not self.child_types:
            self.child_types = (Bubble,)
        for name, value in kwargs.items():

            setattr(self, name, value)
        self._init_make_callable("music")
        self._init_make_callable("sequence")
        self._init_append_children()


    def __setitem__(self, arg, bubble):
        if inspect.isclass(bubble):
            bubble = bubble()
        if type(arg) is slice:
            # needed for base TreeContainer implementation:
            abjad.datastructuretools.TreeContainer.__setitem__(self, arg, bubble)
        elif not isinstance(bubble, self.child_types):
            print(type(arg))
            print(bubble)
            self.warn("attempted to add child but not an allowed child type - attribute/child not added", bubble)
        else:
            if type(arg) is int:
                # if setting based on integer index or slice, use abjad's tree container default behavior
                abjad.datastructuretools.TreeContainer.__setitem__(self, arg, bubble)
            else:
                bubble.name = arg
                setattr(self, arg, bubble)
                new_child = True

                for i, b in enumerate(self.children):
                    if b.name == arg:
                        abjad.datastructuretools.TreeContainer.__setitem__(self, i, bubble)
                        new_child = False
                        break
                if new_child:
                    abjad.datastructuretools.TreeContainer.__setitem__(self,
                        slice(len(self), len(self)),
                        [bubble]
                        )

    # TO DO... used? depreciate?
    def index_children(self):
        for i, child in enumerate(self.children):
            child.original_index = i
            child.original_depthwise_index = child.depthwise_index # TO DO... this could get expensive

    @property
    def my_index(self):
        return self.parent.index(self)
        # return self.graph_order[-1] # NOTE... this does the same thing... which performs better??


    @property
    def depthwise_index(self):
        """
        Not sure how well this performs, but it works
        """
        return self.root.depthwise_inventory[self.depth].index(self)

    # TO DO... is this every used?
    def copy(self):
        new_self = deepcopy(self)
        # for child in self.children:
        #     new_self.append(child.copy())
        return new_self

    # TO DO: still needed?
    def branch(self, *args, **kwargs):
        """
        creates a child object of type self.children_type (appending the child to self), and returns the appended child
        """
        new_branch = self.child_types[0](*args, **kwargs)
        self.append( new_branch )
        return new_branch

    # TO DO.. depreciate?
    def setup(self, **kwargs):
        """
        hook that's called at end of bubble __init__ method (just before arrange), 
        for adjusting bubble atributes / actual bubble material, etc.
        """
        pass

    # # TO DO.. depreciate?
    # def arrange(self, **kwargs):
    #     """
    #     hook that's called at end of bubble __init__ method, for arranging music
    #     (usually dealing with bubble attributes... adding articulations, phrasing, etc.)
    #     """
    #     pass

    # # TO DO... depreciate?
    # def latch(self, **kwargs):
    #     return_bubble = copy(self)
    #     for name, value in kwargs.items():
    #         setattr(return_bubble, name, value)
    #     return return_bubble

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

    def after_music(self, music, **kwargs):
        # TO DO... is this the best place for respell, etc.?
        if self.respell:
            tools.respell(music, self.respell)
        # TO DO... look at these process_methods in light of "machines" work in copper
        for m in self.process_methods:
            m(music)

    def blow(self, **kwargs):
        my_music = self.music()
        self.after_music(my_music)
        # TO DO... depreciate commands?
        # for c in self.commands:
        #     command = indicatortools.LilyPondCommand(c[0], c[1])
        #     attach(command, my_music)
        return my_music

    def warn(self, msg, data=None, **kwargs):
        print("WARNING - %s: %s" % (self.__class__.__name__, msg)  )
        if data is not None:
            print(data)
        print("------------------------------")

    def info(self, msg, data=None, **kwargs):
        print("INFO - %s: %s" % (self.__class__.__name__, msg)  )
        if data is not None:
            print(data)
        print("------------------------------")

    def verify(self, condition, msg=None, data=None, **kwargs):
        if not condition:
            self.warn(msg or "(no message)", data)
        return condition

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

    @classmethod
    def class_sequence(cls, **kwargs):
        my_sequence = []

        # # This adds all bubble classes to the sequence, in the defined order:
        class_hierarchy = inspect.getmro(cls)[::-1]
        child_types = cls.child_types or (Bubble, )

        for c in class_hierarchy:
            if issubclass(c, Bubble):
                for name, attr in c.__dict__.items():
                    if inspect.isclass(attr) and issubclass(attr, child_types) and not name in my_sequence:
                        my_sequence.append(name)
                    elif isinstance(attr, child_types):
                        my_sequence.append(name)

        # # # # This adds all bubble instances to the sequence, also in the defined order
        # # # # NOTE that instances will always follow AFTER classes...
        # # # # TO DO... is this needed????
        # if bubble is not None:
        #     # print(dir(bubble))
        #     for b in bubble.__dict__:
        #         if isinstance( getattr(bubble, b), bubble.child_types):
        #             my_sequence.append(b)

        # print(cls.__definition_order__)
        return my_sequence

    def sequence(self, **kwargs):
        # my_sequence = self.class_sequence(**kwargs) #+ self.added_bubbles
        return [b.name for b in self.children]

    def blow_bubble(self, bubble_name):
        """
        execute for each bubble attribute to add that bubble's music to the main bubble's music
        """
        bubble = getattr(self, bubble_name, None)
        if bubble:
            if inspect.isclass(bubble):
                # if bubble is a class, then we want to get an instance of that class...
                bubble = bubble()
            # if isinstance(bubble, Placeholder) and hasattr(self, "bubble_default"):
            #     bubble = self.bubble_default   
            # print(type(bubble.blow()))   
            return self.bubble_imprint( bubble.blow() )

    # TO DO.. depreciate? (but currently used in MultiLine)
    def bubble_imprint(self, music):
        return music

    def music(self, **kwargs):
        my_music = self.music_container()
        for bubble_name in self.sequence():
            # the bubble attribute specified by the sequence must exist on this bubble object...
            append_music = self.blow_bubble(bubble_name)
            my_music.append(append_music)
        return my_music
