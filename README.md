## comma.ai command-line additions and practical tooling for all

improving the dev workflow friction is paramount to innovating [openpilot](https://github.com/commaai/openpilot)

***PRs accepted!** What cool shit do you do to your ssh session with your car??*

This tool was created by [Alice Knag](https://github.com/AskAlice) - `@emu#6969` on Discord, and is widely contributed to by [ShaneSmiskol](https://github.com/ShaneSmiskol) - `Shane#6175`
If you have any questions about the development process, or have any ideas you want to see happen, check out [CONTRIBUTING.md](CONTRIBUTING.md) and/or DM one of us on Discord or ask in #custom-forks
<p align="center">
  <img src="https://emu.bz/bh8" alt="" />
  <a href="https://i.imgur.com/Bbr1sPX.mp4">
  <img src="https://thumbs.gfycat.com/LimpDeadIaerismetalmark-size_restricted.gif" alt="click for full size">
  <br/>Click for Full Size</a>
</p>

# Getting Started

To install these utilities, SSH into your comma device running neos (ie Comma 2, Eon, etc), and paste in the following:
```bash
bash <(curl -fsSL install.emu.sh) # the brain of the bird
source /data/community/.bashrc
```

<!-- <img src="https://thumbs.gfycat.com/DopeyHairyGeese-size_restricted.gif" alt ="" /> -->

---
Read the README for <https://github.com/b-ryan/powerline-shell>. You will need to [install the fonts on the computer/terminal emulator that you SSH from](https://github.com/powerline/fonts)

Alternately, you can install [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts), as it provides more icons than powerline fonts, and is more maintained.

Once NEOS 15 comes out, zsh will be used and [powerlevel10k](https://github.com/romkatv/powerlevel10k) will be the optimal powerline

The default directory of your bash/ssh session is now `/data/openpilot`. Much easier to git pull after shelling in.

# welcome to the family

<img src="https://emu.bz/gay" alt="" height="250px" />

Emu my neo!
You should now be able to use the `emu` command.

# Updating

Once you've installed, you can update via the utility

```bash
emu update
```

This will essentially perform a git pull and replace all current files in the `/data/community/.oh-my-comma` directory with new ones, if an update is available, as well as check the integrity of the files that must remain elsewhere on the filesystem such as the .bashrc and powerline configs

# Commands

### General
- `emu update`: 🎉 Updates this tool, recommended to restart ssh session
- `emu uninstall`: 👋 Uninstalls emu
### [Forks](#fork-management)
- `emu fork`: 🍴 Manage installed forks, or install a new one
  - `emu fork switch`: 🍴 Switch between any openpilot fork
  - `emu fork list`: 📜 See a list of installed forks and branches
### Panda
- `emu panda`: 🐼 panda interfacing tools
  - `emu panda flash`: 🐼 flashes panda with make recover (usually works with the C2)
  - `emu panda flash2`: 🎍 flashes panda using Panda module (usually works with the EON)
### Debugging
- `emu debug`: de-🐛-ing tools
  - `emu debug controlsd`: 🔬 logs controlsd to /data/output.log by default
- `emu device`: 📈 Statistics about your device
  - `emu device battery`: 🔋 see information about the state of your battery
  - `emu device reboot`: ⚡ safely reboot your device
  - `emu device shutdown`: 🔌 safely shutdown your device
  - `emu device settings`: ⚙ open the Settings app

To see more information about each command and its arguments, checkout the full [command documentation here.](/commands/README.md)

---

# Fork management
When you first run any `emu fork` command, `emu` will ask you to perform a one-time setup of cloning the base repository of openpilot from commaai. This may take a while, but upon finishing the setup you will be able to switch to any openpilot fork much quicker than the time it usually takes to full-clone a new fork the old fashioned way.

For each new fork you install with the `emu fork switch` command, Git is able to re-use blobs already downloaded from commaai/openpilot and other similar installed forks, enabling quicker install times.

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
