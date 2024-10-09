import glob
from os.path import basename, dirname, isfile

from .company import Company
from .document import Document, Documents
from .edgar import Edgar
from .txtml import TXTML
from .xbrl import XBRL, XBRLElement

__version__ = "5.5.1"

modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]
