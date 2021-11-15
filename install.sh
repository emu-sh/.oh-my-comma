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
# bash <(curl -fsSL install.emu.sh) # the brain of the bird
# source $SYSTEM_BASHRC_PATH depending on system

if [ ! -f /EON ] && [ ! -f /TICI ]; then
  echo "Attempting to install on an unsupported platform"
  echo "emu only supports comma.ai devices at this time"
#  exit 1
fi

SYSTEM_BASHRC_PATH=/home/shane/dev/.oh-my-comma/system_bashrc  # $([ -f /EON ] && echo "/home/.bashrc" || echo "/etc/bash.bashrc")
COMMUNITY_PATH=/data/community
COMMUNITY_BASHRC_PATH=/home/shane/dev/.oh-my-comma/default-bashrcs/.bashrc-community  # /data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma
GIT_BRANCH_NAME=master
GIT_REMOTE_URL=https://github.com/emu-sh/.oh-my-comma.git
OMC_VERSION=0.1.17

install_echo() {  # only prints if not updating
  if [ "$update" != true ]; then
    # shellcheck disable=SC2059
    printf "$1\n"
  fi
}

install_community_bashrc() {
  cp "${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community" $COMMUNITY_BASHRC_PATH
  chmod 755 ${COMMUNITY_BASHRC_PATH}
  echo "Copied ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community to ${COMMUNITY_BASHRC_PATH}"
}

# Check system .bashrc path exists
if [ ! -f "$SYSTEM_BASHRC_PATH" ]; then
  echo "Your .bashrc file does not exist at ${SYSTEM_BASHRC_PATH}"
  exit 1
fi

update=false
if [ $# -ge 1 ] && [ $1 = "update" ]; then
  update=true
fi

if [ $update = false ]; then
  [[ "$DEBUG" == 'true' ]] && set -x
fi

if [ ! -d "/data/community" ]; then
  mkdir /data/community
fi

chmod 755 /data/community

if [ ! -d "$OH_MY_COMMA_PATH" ]; then
  echo "Cloning .oh-my-comma"
  git clone -b ${GIT_BRANCH_NAME} ${GIT_REMOTE_URL} ${OH_MY_COMMA_PATH}
fi

install_echo "Remounting .bashrc partition as writable"
if [ -f /EON ]; then
  mount -o rw,remount /system
else
  sudo mount -o rw,remount /
fi

# FIXME: figure out how to install pip packages in AGNOS
if [ -f /EON ] && [ ! -x "$(command -v powerline-shell)" ] && [ $update = false ]; then
  echo "Do you want to install powerline? [You will also need to install the fonts on your local terminal.]"
  read -p "[Y/n] > " choices
  case ${choices} in
    y|Y ) pip install powerline-shell;;
    * ) echo "Skipping...";;
  esac
fi

install_echo "\nInstalling emu utilities"
# If community .bashrc is sourced, do nothing, else merely append source line to system .bashrc
if grep -q "$SYSTEM_BASHRC_PATH" -e "source ${COMMUNITY_BASHRC_PATH}"; then
  install_echo "Community .bashrc is sourced in system .bashrc, skipping"
else
  # Append community .bashrc source onto system .bashrc
  echo "Sourcing community .bashrc in system .bashrc"
  printf "\n# automatically added by .oh-my-comma:\n%s\n" "source ${COMMUNITY_BASHRC_PATH}" >> "$SYSTEM_BASHRC_PATH"
  echo "Done!"
fi

# FIXME: not applicable on TICI
if [ -f /EON ]; then
  install_echo "Checking /home/.config symlink..."
  if [ "$(readlink -f /home/.config/powerline-shell)" != "$OH_MY_COMMA_PATH/.config/powerline-shell" ]; then
    echo "Creating a symlink of ${OH_MY_COMMA_PATH}/.config/powerline-shell to /home/.config/powerline-shell"
    ln -s ${OH_MY_COMMA_PATH}/.config/powerline-shell /home/.config/powerline-shell
  else
    install_echo "Symlink check passed"
  fi
fi

install_echo "Remounting .bashrc partition as read-only"
if [ -f /EON ]; then
  mount -o r,remount /system
else
  sudo mount -o ro,remount /
fi

# If community .bashrc file doesn't exist, copy from .bashrc-community
if [ ! -f "$COMMUNITY_BASHRC_PATH" ]; then
  echo "Creating your community .bashrc at ${COMMUNITY_BASHRC_PATH}"
  install_community_bashrc
elif [ $update = false ]; then
  echo "A community .bashrc file already exists at ${COMMUNITY_BASHRC_PATH}, but you're installing .oh-my.comma"
  echo "Would you like to overwrite it with the default to make sure it's up to date?"
  read -p "[Y/n]: " overwrite
  case ${overwrite} in
    n|N ) echo "Skipping...";;
    * ) install_community_bashrc;;
  esac
fi

touch ${COMMUNITY_PATH}/.bash_history
chmod 775 ${COMMUNITY_PATH}/.bash_history

printf "\033[92m"
if [ $update = true ]; then
  printf "Successfully updated emu utilities!\n"
else
  echo "Sourcing ${SYSTEM_BASHRC_PATH} to apply the changes made during installation"
  source "$SYSTEM_BASHRC_PATH"
  printf "\nSuccessfully installed emu utilities\n\n"
fi

CURRENT_BRANCH=$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)
if [ "${CURRENT_BRANCH}" != "master" ]; then
  printf "\n\033[0;31mWarning:\033[0m your current .oh-my-comma git branch is %s. If this is unintentional, run:\n\033[92mgit -C /data/community/.oh-my-comma checkout master\033[0m\n" "${CURRENT_BRANCH}"
fi

install_echo "Current version: $OMC_VERSION"  # prints in update.sh
if [ $update = false ]; then
  printf "\033[0mYou may need to run the following to initialize emu:\n\033[92msource %s/emu.sh\n" "${OH_MY_COMMA_PATH}"
fi

printf "\033[0m\n"  # reset color

if [ $update = false ]; then
  set +x
fi
