## Comma neOS powerline prompt and helper commands

PRs accepted! What cool shit do you do to your ssh session with your car??

<img src="https://emu.bz/xmf" alt="" />

# Getting Started
```
mount -o rw,remount /system
pip install powerline-shell
cd /home
git clone https://github.com/ShaneSmiskol/comma-dotfiles
./comma-dotfiles/install.sh
```
**Note, running `install.sh` assumes you used the above command to clone this repository to `/home/comma-dotfiles`.**

# Updating
To update `comma-dotfiles`, run `update.sh` with something like:
```
./home/comma-dotfiles/update.sh
```
This will essentially perform a git pull and replace all current files in the `/home` directory with new ones, if an update is available.

---
Read the README for https://github.com/b-ryan/powerline-shell. You will need to [install the fonts for your terminal](https://github.com/powerline/fonts)

The goal is to get `.bashrc` and the `.config` folder in the `/home/` folder

The default directory of your bash/ssh session is now `/data/openpilot`. Much easier to git pull after shelling in!

# Commands
### Panda
- `pandaflash`: Flashes the panda
- `pandaflash2`: Flashes the panda without `make recover`

### Debugging
- `controlsdebug`: You can debug controlsd and output it to a log of `/data/output.log`

# Git config
While you're in a rw filesystem, you might as well edit your git config so you can push your changes up easily.
```
git config --global user.name "your_username"
git config --global user.email "your_email_address@example.com"
git config --global credential.helper store
git pull
```
