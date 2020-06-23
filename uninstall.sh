#!/usr/bin/bash

# COMMUNITY_PATH=/data/community  # probably shouldn't remove since it will hold forks in the future
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma

#echo "Deleting $COMMUNITY_BASHRC_PATH"
#rm $COMMUNITY_BASHRC_PATH
sed -i.bak.$(date +"%Y-%m-%d-%T") -e  '/^## BEGIN \.oh-my-comma magic ###/,/^### End of \.oh-my-comma magic ###/d' ${COMMUNITY_BASHRC_PATH}
echo "Deleting $OH_MY_COMMA_PATH"
rm -rf $OH_MY_COMMA_PATH

echo "Uninstalled!"
