# import importlib
import inspect, os
import abjad
import calliope

class SetAttributeMixin(object):
    def __init__(self, **kwargs):
        super().__init__()
        for name, value in kwargs.items():
            setattr(self, name, value)

def illustrate_me(
            bubble = None,
            score_type = None,
            force = False, # if true, will create illustration even if called from another module
            **kwargs
            ):

    calling_info = inspect.stack()[1]
    calling_module_path = calling_info[1]
    calling_module_name = os.path.split(calling_module_path)[1].split(".")[0]
    calling_module = inspect.getmodule( calling_info[0] )

    # only illustrate if being called from main module (as opposed to import)
    if not calling_module or calling_module.__name__ == "__main__" or force:

        if bubble is None:
            bubble = calliope.ModuleBubble(module=calling_module)
        elif inspect.isclass(bubble):
            bubble = bubble()

        score_type = score_type or calliope.AutoScore
        my_score = score_type( bubble )

        bubble.illustrate_me(path=calling_module_path, filename=calling_module_name)
