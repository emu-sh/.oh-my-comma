#!/bin/sh
cd /data
mkdir community
cd community
echo "Cloning..."
git clone -b devel https://github.com/AskAlice/.oh-my-comma.git
cd .oh-my-comma
SYSTEM_BASHRC_PATH=/home/.bashrc
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma
COMMUNITY_PROFILE_PATH=/data/community/.comma-profile.sh
read -p "Do you want to install powerline? (y/n) [You will also need to install the fonts on your local terminal.]  >" choice
case $choices in
  y|Y ) pip install powerline-shell;;
  * ) echo "Skipping...";;
esac
echo "Installing emu utilities..."
if [ -f "$SYSTEM_BASHRC_PATH" ]; then
  echo "Your system /home/.bashrc exists..."
  if  [grep -q '/home/.bashrc' -e 'source /data/community/.bashrc']; then
    echo "Found an entry point point for ${COMMUNITY_BASHRC_PATH} in ${SYSTEM_BASHRC_PATH}, skipping changes to /system"
  else
    echo "Your bashrc file is different than the one on the repo. neos 15 will redirect all users to store their bashrc in /data/community"
    echo "remounting /system as rewritable (until neos 15)"
    mount -o rw,remount /system
    echo "moving your current bashrc to /data/community"
    mv ${SYSTEM_BASHRC_PATH} ${COMMUNITY_BASHRC_PATH}
    echo "Copying .bashrc that sources local bashrc to system partition (wont be needed in neos 15)"
    cp ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-system ${SYSTEM_BASHRC_PATH}
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


if [ -f "$COMMUNITY_BASHRC_PATH" ]; then
  if [grep -q '/data/community/.bashrc' -e 'source /data/community/.oh-my-comma/emu-utils.sh']; then
    echo "Skipping community .bashrc installation as it already sources .oh-my-comma's entrypoint"
  else
    echo "Your community bashrc is different than what we've got in this repo... Echoing out our entry point to the bottom of your bashrc in /data/community/.bashrc"
    echo "$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)" >> ${COMMUNITY_BASHRC_PATH}
  fi
else
  echo "Creating user .bashrc to ${COMMUNITY_BASHRC_PATH}"
  touch ${COMMUNITY_BASHRC_PATH}
  echo -e '#!/bin/sh' >> ${COMMUNITY_BASHRC_PATH}
  echo "$(cat ${OH_MY_COMMA_PATH}/default-bashrcs/.bashrc-community)" >>  ${COMMUNITY_BASHRC_PATH}
  echo "cd /data ; cd /data/openpilot  # just in case openpilot is missing, default to /data \
  #This is your space to configure your terminal to your liking \
  " >> ${COMMUNITY_BASHRC_PATH}
fi

source /home/.bashrc
