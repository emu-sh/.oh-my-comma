cd /data ; cd /data/openpilot  # just in case openpilot is missing, default to /data

if [ -x "$(command -v powerline-shell)" ]; then
  source /home/.powerline
fi

function _pandaflash() {
  cd /data/openpilot/panda/board && make recover
}

function _pandaflash2() {
  cd /data/openpilot/panda; pkill -f boardd; PYTHONPATH=..; python -c "from panda import Panda; Panda().flash()"
}

function _controlsdebug(){
  pkill -f controlsd ; PYTHONPATH=/data/openpilot python /data/openpilot/selfdrive/controls/controlsd.py 2>&1 | tee /data/output.log
}

function _installfork(){
  if [ $# -lt 1 ]; then
    echo "You must specify a fork URL to clone!"
    return 1
  fi
  old_count=0
  if [ -d "/data/openpilot.old" ]; then
    while [ -d "/data/openpilot.old${old_count}" ]; do
      old_count=$((old_count+1))
    done
  fi
  echo "using: /data/openpilot.old${old_count}"
  #echo "Moving current openpilot installation to /data/openpilot.old"
  #mv /data/openpilot /data/openpilot.old
  #echo "Fork will be installed to /data/openpilot"
  #git clone $1 /data/openpilot
}

function _updatedotfiles(){
  git -C /home/comma-dotfiles pull ; python /home/comma-dotfiles/install.py
}

function emu(){  # main wrapper function
  commands="
  - update: updates this tool, requires restart of ssh session
  - pandaflash: flashes panda
  - pandaflash2: flashes panda without make recover
  - debug: debugging tools
  - installfork: Specify the fork URL after. Moves openpilot to openpilot.old"
  debugging_commands="
  - controls: logs controlsd to /data/output.log"

  if [ $# -lt 1 ]; then
    printf "You must specify a command for dotfiles. Some options are:"
    printf '%s\n' "$commands"
    return 1
  fi

  if [ $1 = "update" ]; then
    _updatedotfiles
  elif [ $1 = "pandaflash" ]; then
    _pandaflash
  elif [ $1 = "pandaflash2" ]; then
    _pandaflash2
  elif [ $1 = "installfork" ]; then
    _installfork $2
  elif [ $1 = "debug" ]; then
    if [ $# -lt 2 ]; then  # verify at least two arguments
      printf "You must specify a command for dotfiles debug. Some options are:"
      printf '%s\n' "$debugging_commands"
      return 1
    fi

    if [ $2 = "controls" ]; then
      _controlsdebug
    else
      printf "Unsupported debugging command! Try one of these:"
      printf '%s\n' "$debugging_commands"
    fi
  else
    printf "Unsupported command! Try one of these:"
    printf '%s\n' "$commands"
  fi
}
