Release 0.1.17 (2021-11-17)
=====

* Support comma three, which has its .bashrc located elsewhere.
* Nicer user-facing installation process
* Clean up installation logic:
  * Minimal modification to the system .bashrc file, only one `source` line is appended to the community .bashrc
  * Much safer: the previous installer moved the system .bashrc file to a permanently rw partition

Release 0.1.16 (2021-04-18)
=====

* Add `emu debug reload` (or simply `reload`) command to restart openpilot without needing to reboot your device.


Release 0.1.15 (2021-04-11)
=====

* Add `repo` flag to `emu fork switch` command: if a repository's name isn't openpilot and isn't a GitHub fork (no name redirection), you can use this option the first time you switch to the fork (remembers URL after that).


Release 0.1.14 (2021-04-02)
=====

* Remember user's GitHub credentials for 1 day (for pushing)
* When `git push`ing, Git will no longer bother you about your local branch's name not matching the remote's
  * You need to re-set up fork management for these two improvements
* Fix issue where it would lock user out from `ssh` if a `/openpilot` directory doesn't exist
  * You need to apply the changes manually in your `/data/community/.bashrc` file from [this commit](https://github.com/emu-sh/.oh-my-comma/commit/ea67a5960cf3e4aeb93627060ca4ed990a71f595)


Release 0.1.13 (2021-02-22)
=====

* Add flag to `emu device settings -c` to close settings app
* Use most similar remote branch (using difflib) if user types unknown close branch
* Use existing function in CommandBase for getting flags, exits if fails so no need to catch errors in each command that has flags
* Alias `fork` to `emu fork switch`. Ex.: `fork stock -b devel`


Release 0.1.12 (2020-10-22)
=====

* Force reinitializes when submodules detected on the branch we're switching to
  * Fixes openpilot not starting when switching away and back to a branch with submodule
* Show what git is doing when switching branches (make checkout verbose)
* Speed up switching by ~300ms by only pruning once every 24 hrs.
* Add `--force` flag to switch command, same as `git checkout -f`
* Fix `shutdown` command happily taking any argument without error, defaulting to shutdown when not `-r`
* Add x emoji (❌) prepended to all errors using error function, makes errors stand out more.


Release 0.1.11 (2020-10-05)
=====

* Don't fetch in new sessions while cloning
* Clean up update screen
* Exception catching:
  * When user enters branch for fork switch without the -b flag
  * KeyboardInterrupt exception while cloning

Release 0.1.10 (2020-08-28)
=====

* On first setup we now rename local branch `release2` to `commaai_release2`  (removes dangling `release2` branch after setup and switching to stock)
  * We also now add the `release2` branch to `installed_branches` for the fork so `emu fork list` now shows current branch after immediate set up with no switching
* Add `dragonpilot` as an alias to `dragonpilot-community/dragonpilot`

Release 0.1.9 (2020-08-12)
=====

* Fix "branch you specified does not exist" error due to deleted remote branches
  * Also add a prompt to prune the local branches that have deleted on the remote

Release 0.1.8 (2020-07-29)
=====

* Run user's switch command after fork management setup
* More verbose fork switching, shows git output
* Only print newline when more information about command is available to better differentiate between commands

Release 0.1.7 (2020-07-24)
=====

* Auto updater will check for updates. This is based on .oh-my-zsh's [check_for_upgrade.sh](https://github.com/ohmyzsh/ohmyzsh/blob/master/tools/check_for_upgrade.sh)

Release 0.1.6 (2020-07-23)
=====

* Add device command aliases: battery, settings, shutdown

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
