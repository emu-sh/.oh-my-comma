## comma.ai command-line additions and practical tooling for all

improving the dev workflow friction is paramount to innovating openpilot

***PRs accepted!** What cool shit do you do to your ssh session with your car??*

This repo is very much in active development! Expect it to evolve greatly over the next few weeks

<img src="https://emu.bz/xmf" alt="" />

# Getting Started

```bash
bash <(curl -fsSL install.emu.sh) # the brain of the bird
source /home/.bashrc
```

<img src="https://thumbs.gfycat.com/DopeyHairyGeese-size_restricted.gif" alt ="" />

# welcome to the family

<img src="https://emu.bz/gay" alt="" height="250px" />

You should now be able to use the `emu` command.

# Updating

Once you've installed, you can update via the utility

```bash
emu update
```

This will essentially perform a git pull and replace all current files in the `/data/community/.oh-my-comma` directory with new ones, if an update is available, as well as check the integrity of the files that must remain elsewhere on the filesystem such as the .bashrc and powerline configs

---
Read the README for <https://github.com/b-ryan/powerline-shell.> You will need to [install the fonts on the computer/terminal emulator that you SSH from](https://github.com/powerline/fonts)

The default directory of your bash/ssh session is now `/data/openpilot`. Much easier to git pull after shelling in.

# Commands

### General

- `emu fork install https://github.com/...`: Clones the fork URL to `/data/openpilot`. Current folder is moved to `/data/openpilot.old` before cloning

### Panda

- `emu panda flash`: Flashes the panda
- `emu panda flash2`: Flashes the panda without `make recover`

### Debugging

- `emu debug controls`: You can debug controlsd and output it to a log file `/data/output.log`

# Git config

In a rw filesystem, you can edit your git config so you can push your changes up easily.

```bash
mount -o rw,remount /system
git config --global user.name "your_username"
git config --global user.email "your_email_address@example.com"
git config --global credential.helper store
git pull
mount -o r,remount /system
```

if the git pull fails, just do some action on git that requires authentication, and you should be good to go
