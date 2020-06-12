#!/bin/bash
SYSTEM_BASHRC_PATH=/home/.bashrc
export COMMUNITY_PATH=/data/community
export COMMUNITY_BASHRC_PATH=/data/community/.bashrc
export OH_MY_COMMA_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source ${OH_MY_COMMA_PATH}/powerline.sh

commands="
  - update: updates this tool, requires restart of ssh session
  - pandaflash: flashes panda
  - pandaflash2: flashes panda without make recover
  - debug: debugging tools
  - installfork: Specify the fork URL after. Moves openpilot to openpilot.old
  - opEdit: Opens the opParams editing interface"
debugging_commands="
  - controls: logs controlsd to /data/output.log"

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

  old_dir="/data/openpilot.old"
  old_count=0
  if [ -d $old_dir ]; then
    while [ -d "/data/openpilot.old.${old_count}" ]; do
      old_count=$((old_count+1))  # counts until we find an unused dir name
    done
    old_dir="${old_dir}.${old_count}"
  fi

  echo "Moving current openpilot installation to ${old_dir}"
  mv /data/openpilot ${old_dir}
  echo "Fork will be installed to /data/openpilot"
  git clone $1 /data/openpilot
}

function _debug(){
  if [ $# -lt 1 ]; then  # verify at least two arguments
    printf "You must specify a command for emu debug. Some options are:"
    printf '%s\n' "$debugging_commands"
    return 1
  fi

  if [ $1 = "controls" ]; then
    _controlsdebug
  else
    printf "Unsupported debugging command! Try one of these:"
    printf '%s\n' "$debugging_commands"
  fi
}

function _opedit() {
  opEditFile=/data/openpilot/op_edit.py
  if [ -f "$opEditFile" ]; then
    python $opEditFile
  else
    echo "Error, current installed fork doesn't have opEdit!"
  fi
}

function _updateohmycomma(){
  source /data/community/.oh-my-comma/update.sh
}

function emu(){  # main wrapper function
  if [ $# -lt 1 ]; then
    printf "You must specify a command for emu. Some options are:"
    printf '%s\n' "$commands"
    return 1
  fi

  command="${1,,}"
  if [ $command = "update" ]; then
    _updateohmycomma
  elif [ $command = "pandaflash" ]; then
    _pandaflash
  elif [ $command = "pandaflash2" ]; then
    _pandaflash2
  elif [ $command = "installfork" ]; then
    _installfork $2
  elif [ $command = "debug" ]; then
    _debug $2
  elif [ $command = "opedit" ]; then
    _opedit
  else
    printf "Unsupported command! Try one of these:"
    printf '%s\n' "$commands"
  fi
}
