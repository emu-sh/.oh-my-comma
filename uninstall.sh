#!/usr/bin/bash

SYSTEM_BASHRC_PATH=/home/.bashrc
# COMMUNITY_PATH=/data/community  # probably shouldn't remove since it will hold forks in the future
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma

rm $SYSTEM_BASHRC_PATH
rm $COMMUNITY_BASHRC_PATH
rm -rf $OH_MY_COMMA_PATH

echo "Uninstalled!"
