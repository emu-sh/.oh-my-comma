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

CURRENT_BRANCH=$(cd ${OH_MY_COMMA_PATH} && git rev-parse --abbrev-ref HEAD)
CURRENT_VERSION=$(cd ${OH_MY_COMMA_PATH} && git describe --tags | grep -Po "^v(\d+\.)?(\d+\.)?(\*|\d+)")
CURRENT_REMOTE=$(cd ${OH_MY_COMMA_PATH} && git config --get remote.origin.url)

echo "Updated ${OH_MY_COMMA_PATH}"
echo "====== FROM ======"
printf "Version \033[92m${PREV_VERSION}\033[0m | branch \033[92m${PREV_BRANCH}\033[0m | remote \033[92m${PREV_REMOTE}\033[0m\n"
printf "Version \033[92m${CURRENT_VERSION}\033[0m | branch \033[92m${CURRENT_BRANCH}\033[0m | remote \033[92m${CURRENT_REMOTE}\033[0m\n"
echo "======= TO ======="

if git -C $OH_MY_COMMA_PATH log --stat -1 | grep -q 'default-bashrcs/.bashrc-community'; then
  if [ "${PREV_VERSION}" = "${CURRENT_VERSION}" ]; then
    printf "\033[92mThe default .bashrc has been updated!\33[38;5;190m The update has not been applied to retain your custom changes.\nTo update and reset your .bashrc, run the command:\n"
    printf "\033[92mcp -fr /data/community/.oh-my-comma/default-bashrcs/.bashrc-community /data/community/.bashrc\n\n"
    printf "\33[38;5;190mThis will wipe any custom changes you've made!\033[0m\n"
  fi
fi