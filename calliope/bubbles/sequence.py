import importlib, inspect
from calliope import bubbles

class BubbleSequence(bubbles.Bubble):
    sequenced_bubbles = ()
    is_simultaneous = False

    def music(self, **kwargs):
        my_music = self.music_container()
        for bubble in self.sequenced_bubbles:
            if inspect.isclass(bubble):
                # if bubble is a class, then we want to get an instance of that class...
                bubble = bubble()
            my_music.append(bubble.blow())
        return my_music

class ModuleSequence(bubbles.Bubble):
    modules = ()
    is_simultaneous = True
    initial_module_bubble = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.modules:
            initial_module = importlib.import_module(*self.modules[0])
            self.initial_module_bubble = bubbles.ModuleBubble(module=initial_module)
        for bubble_name in self.sequence(**kwargs):
            sequenced_bubbles = [ getattr(b, bubble_name, None) for b in self.module_bubbles() ]
            sequenced_bubbles = [ b for b in sequenced_bubbles if b is not None ]
            self[bubble_name] = BubbleSequence(
                    container_type = self.initial_module_bubble.container_type,
                    context_name = self.initial_module_bubble.context_name,
                    sequenced_bubbles = sequenced_bubbles )

    def sequence(self, **kwargs):
        if self.initial_module_bubble:
            return self.initial_module_bubble.sequence(**kwargs)
        else:
            return ()

    def module_bubbles(self):
        if self.initial_module_bubble:
            return_bubbles = [self.initial_module_bubble]
            for m in self.modules[1:]:
                additional_module = importlib.import_module(*m) # TO DO: WTF ??????????
                return_bubbles.append( bubbles.ModuleBubble(additional_module) )
            return return_bubbles
        else:
            return ()



