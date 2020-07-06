import os
import importlib
from py_utils.emu_utils import error


EMU_COMMANDS = []
for module_name in os.listdir(os.path.dirname(__file__)):
    if module_name.endswith('.py') or module_name == '__pycache__':
        continue
    try:
      module = importlib.import_module('emu_commands.{}'.format(module_name))
      module = getattr(module, module_name.title())()
      EMU_COMMANDS.append(module)
    except Exception as e:
      error('Error loading {} command, please try updating!'.format(module_name))
      error(e)
