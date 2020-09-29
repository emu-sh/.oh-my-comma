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
# source /home/.bashrc

SYSTEM_BASHRC_PATH=/home/.bashrc
COMMUNITY_PATH=/data/community
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma
GIT_BRANCH_NAME=master
GIT_REMOTE_URL=https://github.com/emu-sh/.oh-my-comma.git
OMC_VERSION=0.1.9

update_print() {  # only prints if not updating
  if [ "$update" != true ]; then
    echo "$1"
  fi
}

update=false
if [ $# -ge 1 ] && [ $1 = "update" ]; then
  update=true
fi

update_print "THIS IS A TEST!"

if [ $update = false ]; then
  [[ "$DEBUG" == 'true' ]] && set -x
fi

if [ ! -d "/data/community" ]; then
  mkdir /data/community
fi

chmod 755 /data/community

if [ ! -d "$OH_MY_COMMA_PATH" ]; then
  echo "Cloning..."
  git clone -b ${GIT_BRANCH_NAME} ${GIT_REMOTE_URL} ${OH_MY_COMMA_PATH}
fi

echo "Remounting /system as rewritable (until NEOS 15)"
mount -o rw,remount /system

if [ ! -x "$(command -v powerline-shell)" ] && [ $update = false ]; then
  echo "Do you want to install powerline? [You will also need to install the fonts on your local terminal.]"
  read -p "[Y/n] > " choices
  case ${choices} in
    y|Y ) pip install powerline-shell;;
    * ) echo "Skipping...";;
  esac
fi

update_print "\nInstalling emu utilities..."

if [ -f "$SYSTEM_BASHRC_PATH" ]; then
  echo "Your system /home/.bashrc exists..."
  if grep -q '/home/.bashrc' -e 'source /data/community/.bashrc'
  then
    echo "Found an entry point point for ${COMMUNITY_BASHRC_PATH} in ${SYSTEM_BASHRC_PATH}, skipping changes to /system"
  else
    echo "Your bashrc file is different than the one on the repo. NEOS 15 will redirect all users to store their bashrc in /data/community"
    echo "Moving your current bashrc to /data/community"
    mv ${SYSTEM_BASHRC_PATH} ${COMMUNITY_BASHRC_PATH}
    echo "Copying .bashrc that sources local bashrc to system partition (wont be needed in neos 15)"
    cp ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-system ${SYSTEM_BASHRC_PATH}
  fi
else
  echo "Creating a .bashrc in /home/ that sources the community bashrc in /data/community/"
  cp ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-system ${SYSTEM_BASHRC_PATH}
fi

echo "Checking /home/.config symlink..."
if [ `readlink -f /home/.config/powerline-shell` != "$OH_MY_COMMA_PATH/.config/powerline-shell" ]; then
  echo "Creating a symlink of ${OH_MY_COMMA_PATH}/.config/powerline-shell to /home/.config/powerline-shell"
  ln -s ${OH_MY_COMMA_PATH}/.config/powerline-shell /home/.config/powerline-shell
else
  echo "Symlink check passed"
fi

echo "Remounting /system as read-only"
mount -o r,remount /system

#Coping user bashrc, outside of system partition
if [ -f "$COMMUNITY_BASHRC_PATH" ]; then
  #bashrc found
  if grep -q '/data/community/.bashrc' -e 'source /data/community/.oh-my-comma/emu-utils.sh'
  then
    # v0.1.0 -> v0.1.1
    # Test for and patch Backwards compatibility issues with file rename
    if grep -q '/data/community/.bashrc' -e '^### End of \.oh-my-comma magic ###$'
    then
      echo "There's something wrong with your community .bashrc ?? You should copy the one from ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community) to ${COMMUNITY_BASHRC_PATH}"
    else
    # Patch the current bashrc with the updated settings, without destroying user modifications
    echo "Found old entrypoint filename. Removing that line"
    rm .bashrc.lock
    chmod 755 ${COMMUNITY_BASHRC_PATH}
    mv ${COMMUNITY_BASHRC_PATH} ${COMMUNITY_PATH}/.bashrc.lock
    sed -i.bak.$(date +"%Y-%m-%d-%T") -e "/^source \/data\/community\/\.oh-my-comma\/emu-utils\.sh$/d" ${COMMUNITY_BASHRC_PATH}.lock
    echo "$(sed '/### End of \.oh-my-comma magic ###/q' ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)\n$(cat ${COMMUNITY_BASHRC_PATH}.lock)\n" >> ${COMMUNITY_BASHRC_PATH} 
    rm ${COMMUNITY_BASHRC_PATH}.lock
    chmod 755 ${COMMUNITY_BASHRC_PATH}
    fi
  fi

  if grep -q '/data/community/.bashrc' -e 'source /data/community/.oh-my-comma/emu.sh'
  then
    echo "Skipping community .bashrc installation as it already sources .oh-my-comma's entrypoint"
  else
    echo "Your community bashrc is different than what we've got in this repo... Echoing out our entry point to the bottom of your bashrc in /data/community/.bashrc"
    printf "\n$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)\n" >>  ${COMMUNITY_BASHRC_PATH}
  fi
else
  echo "Creating the community .bashrc at ${COMMUNITY_BASHRC_PATH}"
  touch ${COMMUNITY_BASHRC_PATH}
  chmod 755 ${COMMUNITY_BASHRC_PATH}
  printf "$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)\n" >>  ${COMMUNITY_BASHRC_PATH}
fi
touch ${COMMUNITY_PATH}/.bash_history
chmod 775 ${COMMUNITY_PATH}/.bash_history
#Post-install
if [ $update = false ]; then
  printf "    Contents of system bashrc:   \n"
  cat ${SYSTEM_BASHRC_PATH}
  printf "      End of $SYSTEM_BASHRC_PATH       \n\n  Contents of community bashrc:  \n"
  cat ${COMMUNITY_BASHRC_PATH}
  printf " End of $COMMUNITY_BASHRC_PATH  \n\n"
fi

printf "\033[92m"
if [ $update = true ]; then
  printf "Successfully updated emu utilities!\n"
else
  echo "Sourcing /home/.bashrc to apply the changes made during installation"
  source /home/.bashrc
  printf "\nSuccessfully installed emu utilities\n\n"
fi

CURRENT_BRANCH=$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)
#if [ ${CURRENT_BRANCH} != "master" ]; then
#  printf "\n\033[0;31mWarning:\033[0m your current .oh-my-comma git branch is ${CURRENT_BRANCH}. If this is unintentional, run:\n\033[92mgit -C /data/community/.oh-my-comma checkout master\033[0m\n\n"
#fi

echo "Current version: $OMC_VERSION"
printf "\033[0mYou may need to run the following to reflect the update:\n\033[92msource ${OH_MY_COMMA_PATH}/emu.sh"
printf "\033[0m\n\n"

if [ $update = false ]; then
  set +x
fi
