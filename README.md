## Comma neOS powerline prompt and helper commands

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
