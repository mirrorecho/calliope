import importlib
import sys
import inspect

# modules = ["test1","test2"]
# for m in modules:
#   module = importlib.import_module(m)
#   print(dir(module))

# print("BOOO")
# print(sys.modules[__name__])

def yo():
    calling_info = inspect.stack()[1]
    calling_module = inspect.getmodule( calling_info[0] )
    print(dir(calling_module))

yo()