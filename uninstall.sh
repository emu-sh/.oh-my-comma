#!/usr/bin/bash

COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma

remount_system() {
  # Mounts the correct partition at which each OS's .bashrc is located
  writable_str=$([ "$1" = "rw" ] && echo "writable" || echo "read-only")
  if [ -f /EON ]; then
    permission=$([ "$1" = "ro" ] && echo "r" || echo "rw")  # just maps ro to r on EON
    install_echo "ℹ️  Remounting /system partition as ${writable_str}"
    mount -o "$permission",remount /system || exit 1
  else
    install_echo "ℹ️  Remounting / partition as ${writable_str}"
    sudo mount -o "$1",remount / || exit 1
  fi
}

echo "Deleting $COMMUNITY_BASHRC_PATH"
rm $COMMUNITY_BASHRC_PATH

# only applicable on NEOS for now
if [ -f /EON ] && [ -x "$(command -v powerline-shell)" ]; then
  echo "It's recommended to uninstall powerline if you uninstall emu. Uninstall powerline?"
  read -p "[Y/n] > " choices
  case ${choices} in
    n|N ) echo "Skipping...";;
    * ) remount_system rw && pip uninstall powerline-shell || remount_system ro;;
  esac
fi

echo "Deleting $OH_MY_COMMA_PATH"
rm -rf $OH_MY_COMMA_PATH

echo "Uninstalled!"
