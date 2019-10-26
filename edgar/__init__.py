from os.path import dirname, basename, isfile
import glob
from .edgar import Edgar
from .txtml import TXTML
from .company import Company

__version__ = "3.0.0"

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
