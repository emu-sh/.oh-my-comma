#!/usr/bin/bash

COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma

echo "Deleting $COMMUNITY_BASHRC_PATH"
rm $COMMUNITY_BASHRC_PATH

# only applicable on NEOS for now
if [ -f /EON ] && [ -x "$(command -v powerline-shell)" ]; then
  echo "It's recommended to uninstall powerline if you uninstall emu. Uninstall powerline?"
  read -p "[Y/n] > " choices
  case ${choices} in
    n|N ) echo "Skipping...";;
    * ) mount -o rw,remount /system && pip uninstall powerline-shell && mount -o r,remount /system;;
  esac
fi

echo "Deleting $OH_MY_COMMA_PATH"
rm -rf $OH_MY_COMMA_PATH

echo "Uninstalled!"
