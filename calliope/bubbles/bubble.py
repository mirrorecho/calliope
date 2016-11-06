import inspect, collections
import abjad
from calliope import tools, bubbles

# a little metaclass trick to keep class definition order intact.
# ... see: http://stackoverflow.com/questions/4459531/how-to-read-class-attributes-in-the-same-order-as-declared
class OrderedClassMembers(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(self, name, bases, classdict):
        # print(classdict.keys())
        classdict['__ordered__'] = [key for key in classdict.keys()
                if key not in ('__module__', '__qualname__')]
        return type.__new__(self, name, bases, classdict)


class Bubble(metaclass=OrderedClassMembers):
    name=None
    container_type=abjad.Container
    context_name=None
    is_simultaneous=False
    child_types = ()
    commands = ()
    sequence = ()
    respell=None # TO DO, best place for this?
    process_methods = () # TO DO... depreciate?
    stylesheets = ()
    is_simultaneous=True
    added_bubbles = ()

    def make_callable(self, attr_name):
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

    def __init__(self, **kwargs):
        # the first arg is always the music, if passed:
        for name, value in kwargs.items():
            setattr(self, name, value)
        if not self.child_types:
            self.child_types = (Bubble,)
        self.added_bubbles = []
        self.make_callable("music")
        self.make_callable("sequence")
        # self.setup()
        # self.arrange()

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

    def __setitem__(self, bubble_name, bubble):
        if not Bubble.isbubble(bubble):
            self.warn("attempted to add non-bubble object as bubble - attribute not added", bubble_name, bubble)
        else:
            setattr(self, bubble_name, bubble)
            self.added_bubbles.append(bubble_name)

    def __getitem__(self, bubble_name):
        return getattr(self, bubble_name, None)

    # TO DO... this implementation of add/mul creates odd nested containers... rethink
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
        for c in self.commands:
            command = indicatortools.LilyPondCommand(c[0], c[1])
            attach(command, my_music)
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

    def __str__(self):
        music = self.blow()
        return(format(music))

    def get_lilypond_file(self):
        music = self.blow()
        lilypond_file = abjad.lilypondfiletools.make_basic_lilypond_file(music, includes=self.stylesheets, 
            )
        self.info("got abjad representation of lilypond file... now rendering with lilypond")
        return lilypond_file

    @classmethod
    def class_sequence(cls, bubble=None, **kwargs):
        # bubbles = [getattr(self,b) for b in dir(self) if isinstance(getattr(self,b), self.child_types)]
        # bubbles.sort(key=lambda x : x.order)
        bubble = bubble or cls
        my_sequence = []

        # This adds all bubble classes to the sequence, in the defined order:
        class_hierarchy = inspect.getmro(cls)[::-1]
        for c in class_hierarchy:
            if issubclass(c, Bubble):
                for b in c.__ordered__:
                    b_attr = getattr(bubble, b, None)
                    if b_attr and inspect.isclass(b_attr) and issubclass(b_attr, bubble.child_types) and not b in my_sequence:
                        my_sequence.append(b)

        # This adds all bubble instances to the sequence, also in the defined order
        # NOTE that instances will always follow AFTER classes...
        for b in bubble.__ordered__:
            if isinstance( getattr(bubble, b), bubble.child_types):
                my_sequence.append(b)
        
        return my_sequence

    def sequence(self, **kwargs):
        return self.class_sequence(self, **kwargs) + self.added_bubbles

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
