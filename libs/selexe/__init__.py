import warnings

# Show all deprecated warning only once:
warnings.filterwarnings('once', category=DeprecationWarning)
del warnings

__version__ = '0.2.0'

from selexe_runner import SelexeRunner, SelexeError
