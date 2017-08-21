# import importlib
import inspect, os
import abjad
import calliope

def illustrate_me(
            bubble = None,
            score_type = None,
            force = False, # if true, will create illustration even if imported from another module
            **kwargs
            ):

    calling_info = inspect.stack()[1]
    calling_module_file = calling_info[1]
    calling_module_name = os.path.split(calling_module_file)[1].split(".")[0]
    calling_module = inspect.getmodule( calling_info[0] )
    calling_module_directory = os.path.dirname(calling_module_file)

    # only illustrate if being called from main module (as opposed to import)
    if not calling_module or calling_module.__name__ == "__main__" or force:

        if bubble is None:
            bubble = calliope.Bubble.from_module(module=calling_module)
        elif inspect.isclass(bubble):
            bubble = bubble()

        score_type = score_type or calliope.AutoScore
        bubble.illustrate_me(score_type=score_type, directory=calling_module_directory, filename=calling_module_name)
