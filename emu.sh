#!/bin/bash
SYSTEM_BASHRC_PATH=/home/.bashrc
export COMMUNITY_PATH=/data/community
export COMMUNITY_BASHRC_PATH=${COMMUNITY_PATH}/.bashrc
export OH_MY_COMMA_PATH="$(dirname $(readlink -f $0))"

source ${OH_MY_COMMA_PATH}/aliases.sh

function _updateohmycomma(){  # good to keep a backup in case python CLI is broken
  source ${OH_MY_COMMA_PATH}/update.sh
  source ${OH_MY_COMMA_PATH}/emu.sh
}

function emu(){  # main wrapper function
  if $(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))' | grep -q -e '^2')
  then
    python3 "${OH_MY_COMMA_PATH}"/emu.py "$@"
  else
    python "${OH_MY_COMMA_PATH}"/emu.py "$@"
  fi

  if [ $? = 1 ] && [ "$1" = "update" ]; then  # fallback to updating immediately if CLI crashed updating
    printf "\033[91mAn error occurred in the Python CLI, attempting to manually update .oh-my-comma...\n"
    printf "Press Ctrl+C to cancel!\033[0m\n"
    sleep 5
    _updateohmycomma
  fi
}

source ${OH_MY_COMMA_PATH}/check-for-updates.sh
