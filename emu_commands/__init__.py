import glob
import importlib
from py_utils.emu_utils import error
from os.path import dirname, basename, isfile, join


EMU_COMMANDS = []
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
__all__.remove('base')

for module_name in __all__:
  try:
    module = importlib.import_module('emu_commands.{}'.format(module_name))
    module = getattr(module, module_name.title())()
    EMU_COMMANDS.append(module)
  except:
    error('Error loading {} command, please try updating!')
