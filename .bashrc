cd /data/openpilot

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

function _updatedotfiles(){
  git -C /home/comma-dotfiles pull ; python /home/comma-dotfiles/install.py
}

function dotfiles(){
  if [ $# < 1]; then
    echo "You must give a command for dotfiles. Some are\n- update\n- pandaflash\n- debug"
    return [n]
  fi

  if [ $1 = "update" ]; then
    _updatedotfiles

  elif [ $1 = "pandaflash" ]; then
    _pandaflash

  elif [ $1 = "pandaflash2" ]; then
    _pandaflash2

  elif [ $1 = "debug" ]; then
    if [ $2 = "controls" ]; then
      _controlsdebug
    else
      echo "Unsupported debugging command!"
  else
    echo "Unsupported command!"
  fi
}
