import abjad
import calliope

class BaseTransform(calliope.Tree):
    pass # just for inheritance consistency

class Transform(BaseTransform):
    child_types = (BaseTransform, )
    mask = False

    def __init__(self, *args, **kwargs):
        # print(args)
        super().__init__(*args, **kwargs) # TO DO... ??? WTF with args?
        self.setup(**kwargs)

    def __call__(self, selectable, **kwargs):
        if not self.mask:
            self.transform(selectable, **kwargs)

    def transform(self, selectable, **kwargs):
        """
        hook for doing something to the machine
        """
        pass

    @classmethod
    def make(cls, callable, **kwargs):
        my_transform = cls(**kwargs)
        my_transform.transform = callable
        return my_transform



