cd /data/openpilot

if ! [ -x "$(command -v powerline)" ]; then
  source .powerline
fi

function pandaflash() {
  cd /data/openpilot/panda/board && make recover
}

function pandaflash2() {
  cd /data/openpilot/panda; pkill -f boardd; PYTHONPATH=..; python -c "from panda import Panda; Panda().flash()"
}

function controlsdebug(){
  pkill -f controlsd ; PYTHONPATH=/data/openpilot python /data/openpilot/selfdrive/controls/controlsd.py 2>&1 | tee /data/output.log
}
