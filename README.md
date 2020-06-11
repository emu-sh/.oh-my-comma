## Comma neOS powerline prompt and helper commands

PRs accepted! What cool shit do you do to your ssh session with your car??

improving the dev workflow friction is paramount to innovating openpilot

<img src="https://emu.bz/xmf" alt="" />

# Getting Started
```
mount -o rw,remount /system
pip install powerline-shell  # optional!
cd /home
git clone https://github.com/AskAlice/comma-dotfiles
python /home/comma-dotfiles/install.py
```
**Note, running `install.py` assumes you used the above command to clone this repository to `/home/comma-dotfiles`. If you installed `powerline`, it will be automatically detected and the config files will be copied.**

# Updating
To update `comma-dotfiles`, run the `update` command via:
```
dotfiles update
```
This will essentially perform a git pull and replace all current files in the `/home` directory with new ones, if an update is available.

---
Read the README for https://github.com/b-ryan/powerline-shell. You will need to [install the fonts for your terminal](https://github.com/powerline/fonts)

The goal is to get `.bashrc` and the `.config` folder in the `/home/` folder

The default directory of your bash/ssh session is now `/data/openpilot`. Much easier to git pull after shelling in!

# Commands
### General
- `dotfiles installfork https://github.com/...`: Clones the fork URL to `/data/openpilot`. Current folder is moved to `/data/openpilot.old` before cloning

### Panda
- `dotfiles pandaflash`: Flashes the panda
- `dotfiles pandaflash2`: Flashes the panda without `make recover`

### Debugging
- `dotfiles debug controlsd`: You can debug controlsd and output it to a log of `/data/output.log`

# Git config
While you're in a rw filesystem, you might as well edit your git config so you can push your changes up easily.
```
git config --global user.name "your_username"
git config --global user.email "your_email_address@example.com"
git config --global credential.helper store
git pull
```
if the git pull fails, just do some action on git that requires authentication, and you should be good to go
