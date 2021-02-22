#!/usr/bin/python
# -*- coding: utf-8 -*-
from py_utils.colors import COLORS
from py_utils.emu_utils import ArgumentParser, BaseFunctions, success, error


class CommandBase(BaseFunctions):
  def __init__(self):
    self.name = ''
    self.commands = {}

  def main(self, args, cmd_name):
    self.args = args
    cmd = self.next_arg()
    if len(self.commands) > 0:
      if cmd is None:
        self.print_commands(error_msg='You must specify a command for emu {}. Some options are:'.format(cmd_name))
        return
      if cmd not in self.commands:
        self.print_commands(error_msg='Unknown command! Try one of these:')
        return
      self.start_function_from_str(cmd)
    else:
      self.start_function_from_str(cmd_name)  # eg. update and uninstall

  def start_function_from_str(self, cmd):
    cmd = '_' + cmd
    if not hasattr(self, cmd):
      error('Command has not been implemented yet, please try updating.')
      return
    getattr(self, cmd)()  # call command's function

  def parse_flags(self, cmd_name):
    try:
      return self.commands[cmd_name].parser.parse_args(self.args)
    except Exception as e:
      error(e)
      self._help(cmd_name)
      exit()

  def _help(self, cmd, show_description=True, leading=''):
    has_extra_info = False
    description = self.commands[cmd].description
    if show_description:
      print('{}>>  Description 📚: {}{}'.format(COLORS.CYAN, description, COLORS.ENDC))

    flags = self.commands[cmd].flags

    flags_to_print = []
    if flags is not None and len(flags) > 0:
      has_extra_info = True
      usage_req = [f.aliases[0] for f in flags if f.required and len(f.aliases) == 1]  # if required
      usage_non_req = [f.aliases[0] for f in flags if not f.required and len(f.aliases) == 1]  # if non-required non-positional
      usage_flags = [f.aliases for f in flags if not f.required and len(f.aliases) > 1 or f.aliases[0].startswith('-')]  # if flag
      if len(usage_req) > 0 or len(usage_non_req) > 0:  # print usage with proper braces
        usage_req = ['[{}]'.format(u) for u in usage_req]
        usage_non_req = ['({})'.format(u) for u in usage_non_req]
        if len(usage_flags):
          # formats flags to: "[-b BRANCH, -o OUTPUT]"
          usage_flags = ['{} {}'.format(min(u, key=len), max(u, key=len).upper()[2:]) for u in usage_flags]
          usage_flags = ['[{}]'.format(', '.join(usage_flags))]

        usage = ['emu', self.name, cmd] + usage_req + usage_non_req + usage_flags
        print(leading + COLORS.WARNING + '>>  Usage:{} {}'.format(COLORS.OKGREEN, ' '.join(usage)) + COLORS.ENDC)

      print(leading + COLORS.WARNING + '>>  Arguments 💢:' + COLORS.ENDC)
      for flag in flags:
        aliases = COLORS.SUCCESS + ', '.join(flag.aliases) + COLORS.WARNING
        if not flag.required and '-' not in aliases:
          aliases += COLORS.RED + ' (optional)' + COLORS.WARNING
        flags_to_print.append(leading + COLORS.WARNING + '  - {}: {}'.format(aliases, flag.description) + COLORS.ENDC)
      print('\n'.join(flags_to_print))

    commands = self.commands[cmd].commands
    cmds_to_print = []
    if commands is not None and len(commands) > 0:
      print(leading + '{}>>  Commands 💻:{}'.format(COLORS.OKGREEN, COLORS.ENDC))
      for cmd in commands:
        cmds_to_print.append(leading + COLORS.FAIL + '  - {}: {}'.format(cmd, success(commands[cmd].description, ret=True)) + COLORS.ENDC)
      print('\n'.join(cmds_to_print))
    return has_extra_info


class Flag:
  def __init__(self, aliases, description, required=False, dtype='bool'):
    if isinstance(aliases, str):
      self.aliases = [aliases]
    else:
      self.aliases = aliases
    self.description = description
    self.required = required
    self.dtype = dtype
    if self.required and self.aliases[0][0] == '-':
      raise Exception('Positional arguments cannot be required!')


class Command:
  def __init__(self, description=None, commands=None, flags=None):
    self.parser = ArgumentParser()
    self.description = description
    self.commands = commands
    self.has_flags = False
    self.flags = flags
    if flags is not None:
      self.has_flags = True
      for flag in flags:
        # for each flag, add it as argument with aliases.
        parser_args = {}  # handle various conditions
        if not flag.required and flag.dtype not in ['bool']:
          parser_args['nargs'] = '?'

        if flag.dtype != 'bool':
          parser_args['action'] = 'store'
        elif flag.dtype == 'bool':
          parser_args['action'] = 'store_true'

        if flag.dtype == 'bool':  # type bool is not required when store_true
          pass
        elif flag.dtype == 'str':
          parser_args['type'] = str
        elif flag.dtype == 'int':
          parser_args['type'] = int
        else:
          error('Unsupported dtype: {}'.format(flag.dtype))
          return
        self.parser.add_argument(*flag.aliases, help=flag.description, **parser_args)
