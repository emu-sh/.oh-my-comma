#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import importlib
from py_utils.emu_utils import error

EMU_COMMANDS = []
basedir = os.path.dirname(__file__)
for module_name in os.listdir(basedir):
  if module_name.endswith('.py') or module_name == '__pycache__' or not os.path.isdir(os.path.join(basedir, module_name)):
    continue
  try:
    module = importlib.import_module('commands.{}'.format(module_name))
    module = getattr(module, module_name.title())
    EMU_COMMANDS.append(module())
  except Exception as e:
    error('Error loading {} command, please try updating!'.format(module_name))
    error(e)
