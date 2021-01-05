import calliope


from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
from . import *

# calliope.make_library()
# calliope.make_library("my_name") # ... would use "my_name" as namespace instead of "example_lib"
