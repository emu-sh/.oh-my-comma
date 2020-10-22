#!/usr/bin/python
# -*- coding: utf-8 -*-
from commands.base import CommandBase
from py_utils.emu_utils import run, error, input_with_options, UNINSTALL_PATH


class Uninstall(CommandBase):
  def __init__(self):
    super().__init__()
    self.name = 'uninstall'
    self.description = '👋 Uninstalls emu'

  @staticmethod
  def _uninstall():
    print('Are you sure you want to uninstall emu?')
    if input_with_options(['Y', 'n'], 'n')[0] == 0:
      run(['sh', UNINSTALL_PATH])
    else:
      error('Not uninstalling!')
