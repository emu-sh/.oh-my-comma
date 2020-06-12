#!/bin/bash
SYSTEM_BASHRC_PATH=/home/.bashrc
COMMUNITY_PATH=/data/community
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma

update=false
if [ $# -ge 1 ] && [ $1 = "update" ]; then
  update=true
fi

if [ "$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)" != "master" ]; then
  printf "\n\033[0;31mWarning:\033[0m your current .oh-my-comma git branch is $(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD). Run cd /data/community/.oh-my-comma && git checkout master if this is unintentional\n"
fi

if [ ! update ]; then
  [ "$DEBUG" == 'true' ] && set -x
fi

if [ ! -d "/data/community" ]; then
  mkdir /data/community
fi

cd /data/community

if [ ! -d "$OH_MY_COMMA_PATH" ]; then
  echo "Cloning..."
  git clone -b master https://github.com/AskAlice/.oh-my-comma.git
fi

cd ${OH_MY_COMMA_PATH}

if [ ! -x "$(command -v powerline-shell)" ] && [ $update = false ]; then
  echo "Do you want to install powerline? [You will also need to install the fonts on your local terminal.]"
  read -p "[Y/n] > " choices
  case $choices in
    y|Y ) pip install powerline-shell;;
    * ) echo "Skipping...";;
  esac
fi

echo "Installing emu utilities..."

echo "Remounting /system as rewritable (until neos 15)"
mount -o rw,remount /system

if [ -f "$SYSTEM_BASHRC_PATH" ]; then
  echo "Your system /home/.bashrc exists..."
  if grep -q '/home/.bashrc' -e 'source /data/community/.bashrc'
  then
    echo "Found an entry point point for ${COMMUNITY_BASHRC_PATH} in ${SYSTEM_BASHRC_PATH}, skipping changes to /system"
  else
    echo "Your bashrc file is different than the one on the repo. neos 15 will redirect all users to store their bashrc in /data/community"
    echo "moving your current bashrc to /data/community"
    mv ${SYSTEM_BASHRC_PATH} ${COMMUNITY_BASHRC_PATH}
    echo "Copying .bashrc that sources local bashrc to system partition (wont be needed in neos 15)"
    cp ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-system ${SYSTEM_BASHRC_PATH}
  fi
else
  echo "Creating a .bashrc in /home/ that sources the community bashrc in /data/community/"
  cp ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-system ${SYSTEM_BASHRC_PATH}
fi

echo "Checking /home/.config symlink..."
if [ `readlink -f /home/.config` != "$OH_MY_COMMA_PATH/.config" ]; then
  echo "Creating a symlink of ${OH_MY_COMMA_PATH} to /home/.config"
  ln -s ${OH_MY_COMMA_PATH}/.config /home/.config
else
  echo "Symlink check passed"
fi

echo "Remounting /system as read-only"
mount -o r,remount /system

#Coping user bashrc, outside of system partition
if [ -f "$COMMUNITY_BASHRC_PATH" ]; then
  if grep -q '/data/community/.bashrc' -e 'source /data/community/.oh-my-comma/emu-utils.sh'
  then
    echo "Skipping community .bashrc installation as it already sources .oh-my-comma's entrypoint"
  else
    echo "Your community bashrc is different than what we've got in this repo... Echoing out our entry point to the bottom of your bashrc in /data/community/.bashrc"
    printf "$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)\n" >>  ${COMMUNITY_BASHRC_PATH}
  fi
else
  echo "Creating the community .bashrc at ${COMMUNITY_BASHRC_PATH}"
  touch ${COMMUNITY_BASHRC_PATH}
  printf '#!/bin/sh\n' >> ${COMMUNITY_BASHRC_PATH}
  printf "$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)\n" >>  ${COMMUNITY_BASHRC_PATH}
fi

#Post-install
if [ $update = false ]; then
  printf "Contents of system bashrc:\n"
  cat ${SYSTEM_BASHRC_PATH}
  printf "\nEnd of $SYSTEM_BASHRC_PATH\nContents of community bashrc:\n"
  cat ${COMMUNITY_BASHRC_PATH}
  printf "End of $COMMUNITY_BASHRC_PATH\n"
fi

echo "Sourcing /home/.bashrc to init the changes made during installation"
source /home/.bashrc
if [ $update = true ]; then
  printf "\nSuccessfully updated emu utilities!\n"
else
  printf "\nSuccessfully installed emu utilities!\n"
fi


if [ "$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)" != "master" ]; then
  printf "\n\033[0;31mWarning:\033[0m your current .oh-my-comma git branch is $(git rev-parse --abbrev-ref HEAD). Run cd /data/community/.oh-my-comma && git checkout master if this is unintentional\n"
fi

if [ ! update ]; then
  set +x
fi
