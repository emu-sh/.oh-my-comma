## Comma neOS powerline prompt and helper commands

PRs accepted! What cool shit do you do to your ssh session with your car??

<img src="https://emu.bz/xmf" alt="" />

You should be able to get started with something like:
```
mount -o rw,remount /system
pip install powerline-shell
cd /home/
git clone https://github.com/askalice/comma-dotfiles .
```

Read the README for https://github.com/b-ryan/powerline-shell. You will need to install the fonts for your terminal

The goal is to get `.bashrc` and the `.config` folder in the `/home/` folder

The default directory of your bash/ssh session is now /data/openpilot. Much easier to git pull after shelling in!

## Panda Flashing
You can flash the panda by typing
```
pandaflash
```

or alternately (without make recover)
```
pandaflash2
```

## Controlsd Debugging
You can debug controlsd and output it to a log of /data/output.log by typing
```
controlsdebug
```

## Git config
while you're in a rw filesystem, you might as well edit your git config so you can push your changes up easily
```
git config --global user.name "your_username"
git config --global user.email "your_email_address@example.com"
git config --global credential.helper store
git pull
```
