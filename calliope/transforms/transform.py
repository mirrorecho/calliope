import abjad
import calliope

class Transform(calliope.CalliopeBase):
    mask = False

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



