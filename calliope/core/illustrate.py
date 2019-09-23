# import importlib
import inspect, os
import abjad
import calliope

def illustrate(bubble,
    force = False,
    **kwargs
    ):
    """
    Calls illustrate_me on a bubble only if the calling module is __main__
    or force kwarg == True. Useful for modules that might be illustrated
    on their own, but also imported (and not illustrated when imported).
    """
    calling_info = inspect.stack()[1]
    calling_module = inspect.getmodule( calling_info[0] )

    if not calling_module or calling_module.__name__ == "__main__" or force:

        if inspect.isclass(bubble):
            bubble = bubble()

        bubble.illustrate_me(**kwargs)

def illustrate_me(
    bubble = None,
    **kwargs
    ):
    print("*** illustrate_me() NO LONGER SUPPORTED! ***")

    # calling_info = inspect.stack()[1]
    # calling_module_file = calling_info[1]
    # calling_module_name = os.path.split(calling_module_file)[1].split(".")[0]
    # calling_module = inspect.getmodule( calling_info[0] )
    # calling_module_directory = os.path.dirname(calling_module_file)

    # only illustrate if being called from main module (as opposed to import)



