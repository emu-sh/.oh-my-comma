#!/usr/bin/bash

#            _
#         -=(')
#           ;;
#          //
#         //
#        : '.---.__
#        |  --_-_)__)
#        `.____,'
#           \  \       ___ ._ _ _  _ _
#         ___\  \     / ._>| ' ' || | |
#        (       \    \___.|_|_|_|`___|
#                 \
#                 /

# This is the install script for https://emu.sh/
# Located on git at https://github.com/emu-sh/.oh-my-comma
# To install this, ssh into your comma device and paste:
# source <(curl -fsSL install.emu.sh) # the brain of the bird
# source $SYSTEM_BASHRC_PATH depending on system

if [ ! -f /EON ] && [ ! -f /TICI ]; then
  echo "Attempting to install on an unsupported platform"
  echo "emu only supports comma.ai devices at this time"
  exit 1
fi

SYSTEM_BASHRC_PATH=$([ -f /EON ] && echo "/home/.bashrc" || echo "/etc/bash.bashrc")
COMMUNITY_PATH=/data/community
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma
GIT_BRANCH_NAME=master
GIT_REMOTE_URL=https://github.com/emu-sh/.oh-my-comma.git
OMC_VERSION=0.1.17

install_echo() {  # only prints if not updating
  if [ "$update" != true ]; then
    # shellcheck disable=SC2059
    printf -- "$1\n"
  fi
}

install_community_bashrc() {
  # Copies default-bashrcs/.bashrc-community to /data/community/.bashrc
  cp "${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community" $COMMUNITY_BASHRC_PATH
  chmod 755 ${COMMUNITY_BASHRC_PATH}
  echo "✅ Copied ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community to ${COMMUNITY_BASHRC_PATH}"
}

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

# System .bashrc should exist
if [ ! -f "$SYSTEM_BASHRC_PATH" ]; then
  echo "Your .bashrc file does not exist at ${SYSTEM_BASHRC_PATH}"
  exit 1
fi

update=false
if [ $# -ge 1 ] && [ "$1" = "update" ]; then
  update=true
fi

if [ ! -d "/data/community" ]; then
  mkdir /data/community
  chmod 755 /data/community
fi

if [ ! -d "$OH_MY_COMMA_PATH" ]; then
  echo "Cloning .oh-my-comma"
  git clone -b ${GIT_BRANCH_NAME} ${GIT_REMOTE_URL} ${OH_MY_COMMA_PATH}
fi

install_echo "ℹ️  Installing emu utilities\n"
# If community .bashrc is already sourced, do nothing, else merely append source line to system .bashrc
if grep -q "$SYSTEM_BASHRC_PATH" -e "source ${COMMUNITY_BASHRC_PATH}"; then
  install_echo "✅ Community .bashrc is sourced in system .bashrc, skipping"
else
  # Append community .bashrc source onto system .bashrc
  remount_system rw
  echo "ℹ️  Sourcing community .bashrc in system .bashrc"
  msg="\n# automatically added by .oh-my-comma:\nif [ -f ${COMMUNITY_BASHRC_PATH} ]; then\n  source ${COMMUNITY_BASHRC_PATH}\nfi\n"
  if [ -f /TICI ]; then  # need to sudo on AGNOS
    printf "$msg" | sudo tee -a "$SYSTEM_BASHRC_PATH" > /dev/null || exit 1
  else
    printf "$msg" | tee -a "$SYSTEM_BASHRC_PATH" > /dev/null || exit 1
  fi
  remount_system ro
  printf "✅ Success!\n\n"
fi

# If community .bashrc file doesn't exist, copy from .bashrc-community
if [ ! -f "$COMMUNITY_BASHRC_PATH" ]; then
  echo "ℹ️  Creating your community .bashrc at ${COMMUNITY_BASHRC_PATH}"
  install_community_bashrc
elif [ $update = false ]; then
  printf "\n❗ A .bashrc file already exists at ${COMMUNITY_BASHRC_PATH}, but you're installing .oh-my.comma\n"
  printf "Would you like to overwrite it with the default to make sure it's up to date?\n\n"
  read -p "[Y/n]: " overwrite
  case ${overwrite} in
    n|N ) printf "Skipping...\n";;
    * ) install_community_bashrc;;
  esac
fi

touch ${COMMUNITY_PATH}/.bash_history
chmod 775 ${COMMUNITY_PATH}/.bash_history

if [ ! -d /data/community/.oh-my-zsh ] && [ $update = false ]; then
  echo "Do you want to install zsh, .oh-my-zsh, and powerlevel10k? [You will also need to install nerd fonts on your local terminal. see: https://www.nerdfonts.com/font-downloads]"
  read -p "[y/N] > " choices
  case ${choices} in
    y|Y ) apt update && apt install zsh && zsh ${OH_MY_COMMA_PATH}/install-oh-my-zsh.zsh;;
    * ) echo "Skipping...";;
  esac
fi

printf "\n\033[92m"

CURRENT_BRANCH=$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)
if [ "${CURRENT_BRANCH}" != "master" ]; then
  printf "\n❗ \033[0;31mWarning:\033[0m your current .oh-my-comma git branch is %s. If this is unintentional, run:\n\033[92mgit -C /data/community/.oh-my-comma checkout master\033[0m\n\n" "${CURRENT_BRANCH}"
fi

printf "\033[0m\n"  # reset color
install_echo "Current version: $OMC_VERSION"  # prints in update.sh

if [ $update = true ]; then
  echo "✅ Successfully updated emu utilities!"
else
  printf "\033[0mYou may want to exit out of this bash instance to automatically source emu\n"
  echo "✅ Successfully installed emu utilities!"
  set +x
fi
