EMU_COMMANDS = []
import importlib
# import os
# for cmd in os.listdir(os.getcwd()):
#   print(cmd)

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
print(modules)
print(__all__)
for module in __all__:
  if 'base' == module:
    continue
  print(module)
  module = importlib.import_module(module)
  print(dir(module))
  print(module.name)
# from emu_commands.fork import Fork
# from emu_commands.update import Update
# from emu_commands.panda import Panda
# from emu_commands.debug import Debug
# from emu_commands.device import Device
# from emu_commands.uninstall import Uninstall
#
#
# EMU_COMMANDS = [Fork(), Update(), Panda(), Debug(), Device(), Uninstall()]
