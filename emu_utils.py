import sys


class Commands:
  # todo: make this a dict and format with a function
  commands = "- update: updates this tool, requires restart of ssh session\n" \
             "- pandaflash: flashes panda\n" \
             "- pandaflash2: flashes panda without make recover\n" \
             "- debug: debugging tools\n" \
             "- installfork: Specify the fork URL after. Moves openpilot to openpilot.old"

  debugging_commands = "- controls: logs controlsd to /data/output.log"


class Emu:
  def __init__(self, args):
    self.args = args
    self.parse()

  def parse(self):
    print(sys.argv)


if __name__ == "__main__":
  emu = Emu(sys.argv[1:])
