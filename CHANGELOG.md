Release 0.1.6 (2020-07-22)
=====
* Add device command aliases: battery, settings, shutdown, reboot

Release 0.1.5 (2020-07-22)
=====
* Make the username argument under `emu fork switch` optional. If not specified, it will use the current fork switched to
* Add `--branch` (`-b`) flag for specifying the branch
  * This means you must supply `-b` or `--branch` when switching branches, even when supplying the username:

        Old syntax: emu fork switch another_fork branch
        New syntax: emu fork switch another_fork -b branch

        Old syntax: emu fork switch same_fork new_branch
        New syntax: emu fork switch -b new_branch

Release 0.1.4 (2020-07-12)
=====
* Add `emu device settings` command to open the settings app

Release 0.1.3 (2020-07-06)
=====
* Make flags/arguments more robust. Optional non-positional arguments are now supported, as long as they are the last arguments.
* `emu fork switch` and `emu fork list` commands added. Uses one singular git repo and adds remotes of forks so that the time to install a new fork is reduced significantly since git is able to re-use blobs.
  * A one-time setup is required when using the fork command, this full clones commaai/openpilot which may take a bit of time on first use.
  * Change remote of `origin` to `commaai` so that no additional logic is required. Aliases of stock openpilot are: `['stock', 'commaai', 'origin']`
  * Stores all installed forks and forks' branches in `/data/community/forks.json` so that the forks command can easily identify when it needs to track and create a branch or just check it out.
  * You should still run `git pull` to make sure you get the latest updates from the fork you're currently switched to.
* Dynamic loading of commands. If a command has an exception loading, it won't crash the CLI. Instead you will see an error when you try to call `emu`
