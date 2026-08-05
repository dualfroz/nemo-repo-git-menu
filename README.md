# nemo-repo-git-menu

Git commands in the right click menu of
[Nemo](https://github.com/linuxmint/nemo), the Cinnamon file manager.

| Entry | Runs |
| --- | --- |
| Git Status (terminal) | `git status` |
| Git Log (terminal) | `git log --oneline --graph --decorate -30` |
| Git Fetch (terminal) | `git fetch --all --prune` |
| Git Pull (terminal) | `git pull` |

Each one opens a terminal in the repository root, runs the command, and leaves
the shell open so you can read the output and keep working there.

The entries appear on any folder inside a repository, not only on its root, and
on the empty background of an open folder as well as on the folder icon. On a
folder that is not in a repository nothing is added to the menu.

Nothing here rewrites history or pushes. The most it does is `git pull`.

## Requirements

- [nemo-repo-core](https://github.com/dualfroz/nemo-repo-core) 1.x
- Nemo with `nemo-python`, `git` in `PATH`
- A terminal emulator. `gnome-terminal`, `tilix`, `konsole`, `xfce4-terminal`,
  `mate-terminal`, `kitty`, `alacritty` and `xterm` are detected automatically;
  anything else can be named in the config.

## Install

```bash
git clone https://github.com/dualfroz/nemo-repo-core
cd nemo-repo-core && ./install.sh && cd ..

git clone https://github.com/dualfroz/nemo-repo-git-menu
cd nemo-repo-git-menu && ./install.sh

nemo -q
```

`install.sh` links the plugin into `~/.local/share/nemo-python/extensions` and
checks that it imports. Pass `--copy` to copy instead of link. `./uninstall.sh`
removes it. Nothing is written outside your home directory and no root is
required.

## Configuration

Shared file, read live, no restart needed:

```
~/.config/nemo-repo-core.json
```

```json
{
  "terminal_command": null,
  "actions": {
    "git_status": true,
    "git_log": true,
    "git_fetch": true,
    "git_pull": true
  }
}
```

| Key | Default | Meaning |
| --- | --- | --- |
| `actions.git_status` | `true` | Show the Git Status entry |
| `actions.git_log` | `true` | Show the Git Log entry |
| `actions.git_fetch` | `true` | Show the Git Fetch entry |
| `actions.git_pull` | `true` | Show the Git Pull entry |
| `terminal_command` | `null` | Terminal to use; `null` auto detects. Core setting, shared with the other plugins. |

Turning an entry off takes effect on the next right click.

## Notes

- Commands run in the repository root, not in the folder you clicked, which is
  what makes `git status` from a deep subdirectory show the whole repository.
- The shell that stays open is your `$SHELL`.
- If you use a terminal that is not in the detected list, set
  `terminal_command` to its binary name. Emulators disagree about the flag that
  means "run this command"; unknown ones are called with `-e`, which most of
  them accept.

## Migrating from the single file version

These entries used to be part of `nemo_repo_emblems.py`, one file that also
provided emblems, list view columns and a properties tab. It is now split, and
the split runs along a real line: "Open Terminal Here" and "Open in Editor"
have nothing to do with git and work on any folder, so they moved to
[nemo-folder-tools](https://github.com/dualfroz/nemo-folder-tools). Install
that one too if you used them.

Two changes you will notice: the entries now also appear inside a repository
rather than only on its root, and there is a new Git Fetch entry.

Your config carries over automatically, and the old file is not modified.
Remove the old extension so the entries are not listed twice:

```bash
rm ~/.local/share/nemo-python/extensions/nemo_repo_emblems.py
nemo -q
```

## Tested on

Linux Mint 22.2 (Zara), Cinnamon 6.4.14, Nemo 6.4.5, python-nemo 6.4.0,
Python 3.12.3, with `gnome-terminal`.

## License

MIT. See `LICENSE`.
