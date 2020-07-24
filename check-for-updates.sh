#!/bin/bash

#Based on https://github.com/ohmyzsh/ohmyzsh/blob/master/tools/check_for_upgrade.sh
if [[ "$OMC_DISABLE_AUTO_UPDATE" = true ]] \
   || ! command -v git &>/dev/null; then
    return
fi
OMC_EPOCH=$(date +%s)
set +x
function current_epoch() {
    echo $(($OMC_EPOCH/60/60/24))
}

function update_last_updated_file() {
    echo "LAST_EPOCH=$(current_epoch)" > "${OH_MY_COMMA_PATH}/log/.omc-update"
}
cd ${OH_MY_COMMA_PATH}
OMC_UPSTREAM=${1:-'@{u}'}
OMC_LOCAL=$(git rev-parse @)
OMC_REMOTE=$(git rev-parse "$OMC_UPSTREAM")
OMC_BASE=$(git merge-base @ "$OMC_UPSTREAM")
# Remove lock directory if older than a day
if mtime=$(date +%s -r "$OH_MY_COMMA_PATH/log/update.lock" 2>/dev/null); then
    if (( (mtime + 120) < OMC_EPOCH )); then
        command rm -rf "$OH_MY_COMMA_PATH/log/update.lock"
    fi
fi

# Check for lock directory
if ! command mkdir "$OH_MY_COMMA_PATH/log/update.lock" 2>/dev/null; then
    return
fi

# Remove lock directory on exit. `return 1` is important for when trapping a SIGINT:
#  The return status from the function is handled specially. If it is zero, the signal is
#  assumed to have been handled, and execution continues normally. Otherwise, the shell
#  will behave as interrupted except that the return status of the trap is retained.
trap "command rm -rf '$OH_MY_COMMA_PATH/log/update.lock'; return" EXIT INT QUIT

# Create or update .omc-update file if missing or malformed
if ! source "${OH_MY_COMMA_PATH}/log/.omc-update" 2>/dev/null || [[ -z "$LAST_EPOCH" ]]; then
    touch ${OH_MY_COMMA_PATH}/log/.omc-update
    update_last_updated_file
fi

# Number of days before trying to update again
epoch_target=${OMC_AUTOUPDATE_DAYS:-7}
# Test if enough time has passed until the next update
if (( ( $(current_epoch) - LAST_EPOCH ) < $epoch_target )); then
    return
fi

if [ $OMC_LOCAL != $OMC_BASE ]; then
  # Ask for confirmation before updating unless disabled
  if [[ "$OMC_DISABLE_UPDATE_PROMPT" = true ]]; then
      emu update
  else
      # input sink to swallow all characters typed before the prompt
      # and add a newline if there wasn't one after characters typed
      read -r -p "[emu.sh] Update .oh-my-comma? [Y/n] " option
      [[ "$option" != $'\n' ]] && echo
      case "$option" in
          [yY$'\n']) emu update ;;
          [nN]) update_last_updated_file ;;
        *) update_last_updated_file ;;
      esac
  fi
else
  echo "[emu.sh] Checked for updates, and found none."
fi
cd -
unset -f current_epoch update_last_updated_file

