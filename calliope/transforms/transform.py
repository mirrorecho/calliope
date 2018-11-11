import abjad
import calliope

class Transform(calliope.BaseMixin):
    mask = False

    def __init__(self, **kwargs):
        # print(args)
        super().__init__(**kwargs) 
        self.setup(**kwargs)

    def __call__(self, selectable, **kwargs):
        if not self.mask:
            self.transform(selectable, **kwargs)

    def transform(self, selectable, **kwargs):
        """
        hook for doing something to the machine
        """
        pass

    # TO DO: useful, or KISS?
    # @classmethod
    # def make(cls, callable, **kwargs):
    #     my_transform = cls(**kwargs)
    #     my_transform.transform = callable
    #     return my_transform



