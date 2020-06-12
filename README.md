## Comma neOS powerline prompt and helper commands

PRs accepted! What cool shit do you do to your ssh session with your car??

improving the dev workflow friction is paramount to innovating openpilot

<img src="https://emu.bz/xmf" alt="" />

<img src="https://thumbs.gfycat.com/VapidRipeAquaticleech-size_restricted.gif" alt ="" />

# Getting Started

```
 bash -c "$(curl -fsSL https://raw.githubusercontent.com/AskAlice/.oh-my-comma/master/install.sh)"
 source /home/.bashrc
```

# Updating

Once you've installed, you can update via the utility

```
emu update
```

This will essentially perform a git pull and replace all current files in the `/data/community/.oh-my-comma` directory with new ones, if an update is available.

---
Read the README for <https://github.com/b-ryan/powerline-shell.> You will need to [install the fonts for your terminal](https://github.com/powerline/fonts)

The default directory of your bash/ssh session is now `/data/openpilot`. Much easier to git pull after shelling in.

# Commands

### General

- `emu installfork https://github.com/...`: Clones the fork URL to `/data/openpilot`. Current folder is moved to `/data/openpilot.old` before cloning

### Panda

- `emu pandaflash`: Flashes the panda
- `emu pandaflash2`: Flashes the panda without `make recover`

### Debugging

- `emu debug controls`: You can debug controlsd and output it to a log file `/data/output.log`

# Git config

While you're in a rw filesystem, you might as well edit your git config so you can push your changes up easily.

```
git config --global user.name "your_username"
git config --global user.email "your_email_address@example.com"
git config --global credential.helper store
git pull
```

if the git pull fails, just do some action on git that requires authentication, and you should be good to go
