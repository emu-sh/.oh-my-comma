#!/bin/sh
SYSTEM_BASHRC_PATH=/home/.bashrc
COMMUNITY_PATH=/data/community
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma

if [ ! -d "/data/community" ]; then
  mkdir /data/community
fi

cd /data/community

if [ ! -d "$OH_MY_COMMA_PATH" ]; then
  echo "Cloning..."
  git clone -b devel https://github.com/AskAlice/.oh-my-comma.git
fi

cd ${OH_MY_COMMA_PATH}

if [ ! -x "$(command -v powerline-shell)" ]; then
  read -p "Do you want to install powerline? (y/n) [You will also need to install the fonts on your local terminal.]  >" choice
  case $choices in
    y|Y ) pip install powerline-shell;;
    * ) echo "Skipping...";;
  esac
fi

echo "Installing emu utilities..."
if [ -f "$SYSTEM_BASHRC_PATH" ]; then
  echo "Your system /home/.bashrc exists..."
  if grep -q '/home/.bashrc' -e 'source /data/community/.bashrc'
  then
    echo "Found an entry point point for ${COMMUNITY_BASHRC_PATH} in ${SYSTEM_BASHRC_PATH}, skipping changes to /system"
  else
    echo "Your bashrc file is different than the one on the repo. neos 15 will redirect all users to store their bashrc in /data/community"
    echo "remounting /system as rewritable (until neos 15)"
    mount -o rw,remount /system
    echo "moving your current bashrc to /data/community"
    mv ${SYSTEM_BASHRC_PATH} ${COMMUNITY_BASHRC_PATH}
    echo "Copying .bashrc that sources local bashrc to system partition (wont be needed in neos 15)"
    cp ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-system ${SYSTEM_BASHRC_PATH}
    echo "Creating a symlink of /data/community/.config to /home/.config"
    ln -s /data/community/.config /home/.config
    echo "Creating a symlink of /data/community/.config/powerline-shell to /home/.oh-my-comma/.config/powerline-shell"
    ln -s ${OH_MY_COMMA_PATH}/.config/powerline-shell /data/community/.config/powerline-shell
    echo "remounting /system as read-only"
    mount -o r,remount /system
  fi
else
  echo "remounting /system as rewritable (until neos 15)"
  mount -o rw,remount /system
  echo "Creating a .bashrc in /home/ that sources the community bashrc in /data/community/"
  cp ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-system ${SYSTEM_BASHRC_PATH}
  echo "Creating a symlink of /data/community/.config to /home/.config"
  ln -s /data/community/.config /home/.config
  echo "Creating a symlink of /data/community/.config/powerline-shell to /home/.oh-my-comma/.config/powerline-shell"
  ln -s ${OH_MY_COMMA_PATH}/.config/powerline-shell /data/community/.config/powerline-shell
  echo "remounting /system as read-only"
  mount -o r,remount /system
fi

#Coping user bashrc, outside of system partition
if [ -f "$COMMUNITY_BASHRC_PATH" ]; then
  if grep -q '/data/community/.bashrc' -e 'source /data/community/.oh-my-comma/emu-utils.sh'
  then
    echo "Skipping community .bashrc installation as it already sources .oh-my-comma's entrypoint"
  else
    echo "Your community bashrc is different than what we've got in this repo... Echoing out our entry point to the bottom of your bashrc in /data/community/.bashrc"
    printf "$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)\n\
cd /data ; cd /data/openpilot # just in case openpilot is missing, default to /data\n\n\
# This is your space to configure your terminal to your liking\n\n" >>  ${COMMUNITY_BASHRC_PATH}
  fi
else
  echo "Creating the community .bashrc at ${COMMUNITY_BASHRC_PATH}"
  touch ${COMMUNITY_BASHRC_PATH}
  printf '#!/bin/sh\n' >> ${COMMUNITY_BASHRC_PATH}
  printf "$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)\n\
cd /data ; cd /data/openpilot # just in case openpilot is missing, default to /data\n\n\
# This is your space to configure your terminal to your liking\n\n" >>  ${COMMUNITY_BASHRC_PATH}
fi

#Post-install
printf "Contents of system bashrc:\n"
cat ${SYSTEM_BASHRC_PATH}
printf "\nEnd of $SYSTEM_BASHRC_PATH\nContents of community bashrc:\n"
cat ${COMMUNITY_BASHRC_PATH}
printf "End of $COMMUNITY_BASHRC_PATH\n"

echo "Sourcing /home/.bashrc to init the changes made during installation"
source /home/.bashrc
