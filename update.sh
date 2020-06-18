#!/bin/bash
SYSTEM_BASHRC_PATH=/home/.bashrc
COMMUNITY_PATH=/data/community
COMMUNITY_BASHRC_PATH=/data/community/.bashrc
OH_MY_COMMA_PATH=/data/community/.oh-my-comma
PREV_BRANCH=$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)
PREV_VERSION=$(cd ${OH_MY_COMMA_PATH} && git describe --tags | grep -Po "^v(\d+\.)?(\d+\.)?(\*|\d+)")
PREV_REMOTE=$(cd ${OH_MY_COMMA_PATH} && git config --get remote.origin.url)
git -C ${OH_MY_COMMA_PATH} pull
sh ${OH_MY_COMMA_PATH}/install.sh 'update'
echo "Updated ${OH_MY_COMMA_PATH}"
echo "====== FROM ======"
printf "Version \033[92m${PREV_VERSION}\033[0m / branch \033[92m${PREV_BRANCH}\033[0m / remote \033[92m${PREV_REMOTE}\033[0m\n"
echo "======= TO ======="
CURRENT_BRANCH=$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)
CURRENT_VERSION=$(cd ${OH_MY_COMMA_PATH} && git describe --tags | grep -Po "^v(\d+\.)?(\d+\.)?(\*|\d+)")
CURRENT_REMOTE=$(cd ${OH_MY_COMMA_PATH} && git config --get remote.origin.url)
printf "Version \033[92m${CURRENT_VERSION}\033[0m / branch \033[92m${CURRENT_BRANCH}\033[0m /remote \033[92m${CURRENT_REMOTE}\033[0m\n"
