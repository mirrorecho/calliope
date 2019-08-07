import inspect
import calliope

class TransformFrom(calliope.Factory):
    selectable = None
    transform = calliope.Transform


    def get_branches(self, *args, **kwargs):
        transform = self.transform() if inspect.isclass(self.transform) else self.transform

        return transform(self.selectable())


