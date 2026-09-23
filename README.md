# nemo-repo-git-menu

nemo-repo-git-menu is an extension for [Nemo](https://github.com/linuxmint/nemo),
the Cinnamon file manager, that adds git commands to the right click menu of
folders inside a git repository. Each entry opens a terminal in the repository
root, runs the command and leaves the shell open so the output stays readable.
It is a plugin for **nemo-repo-core** and needs it installed.

## Features

- Four entries:

  | Entry | Runs |
  | --- | --- |
  | Git Status (terminal) | `git status` |
  | Git Log (terminal) | `git log --oneline --graph --decorate -30` |
  | Git Fetch (terminal) | `git fetch --all --prune` |
  | Git Pull (terminal) | `git pull` |

- Entries appear on a single selected folder and on the empty background of an
  open folder, anywhere inside a repository, not only on its root. Commands
  always run in the repository root.
- Nothing is added for folders outside a repository, for remote locations, for
  multiple selections, or when git is not installed.
- Each entry can be switched off in the config; the change applies on the next
  right click.
- The terminal is the core's `terminal_command`, or the first emulator found
  of `gnome-terminal`, `x-terminal-emulator`, `tilix`, `konsole`,
  `xfce4-terminal`, `mate-terminal`, `kitty`, `alacritty`, `xterm`. The shell
  left open afterwards is your `$SHELL`.

## Requirements

- nemo-repo-core 0.1.x
- Nemo with `nemo-python`, `git` and `bash` in `PATH`
- A terminal emulator

## Install and run

Install nemo-repo-core first (run `./install.sh` in its checkout), then from a
checkout of this repository:

```bash
./install.sh
nemo -q
```

`install.sh` links `nemoRepoGitMenu.py` into
`~/.local/share/nemo-python/extensions` and checks that it imports. Pass
`--copy` to copy instead of link. It stops with a message if nemo-repo-core is
not installed. No root is required.
`./uninstall.sh` removes the plugin.

## Configuration

Settings live in the shared file `~/.config/nemo-repo-core.json`.
`config.example.json` shows the keys this plugin uses:

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
| `actions.git_status` | `true` | Show Git Status |
| `actions.git_log` | `true` | Show Git Log |
| `actions.git_fetch` | `true` | Show Git Fetch |
| `actions.git_pull` | `true` | Show Git Pull |
| `terminal_command` | `null` | Core setting: terminal to use; `null` auto detects |

For an emulator that is not in the detected list, set `terminal_command` to its
command. Unknown emulators are called with `-e` to run the command.

## Tests

The tests use the standard library `unittest` and need PyGObject with the Nemo
typelib (`gir1.2-nemo-3.0`) and nemo-repo-core: an installed core, a checkout
of nemo-repo-core next to this one (`../nemo-repo-core`), or a path in
`NEMO_REPO_CORE_PATH`. Without the core the suite is skipped. Run them from the
repository root:

```bash
python3 -m unittest discover -s tests
```

They cover the entries built for repository roots and nested folders, the
exact command and working directory each entry launches, switching entries
off, and which selections get entries. They need neither git nor a terminal: a
stub `.git` directory is used and the terminal launcher is replaced, so nothing
is started. The shared config is redirected to a temporary file, so your real
config is never touched.

## Project layout

```
nemoRepoGitMenu.py        the Nemo extension
config.example.json       keys used by this plugin
install.sh, uninstall.sh  per-user install
tests/
  support.py              temporary config, git helpers and core lookup
  testGitMenu.py          unittest suite
```

## Limitations

- The entries stay visible when no terminal emulator is found; choosing one
  then only logs a warning.
- `terminal_command` is split on single spaces; quoted arguments are not
  supported.
- The command list is fixed; only visibility is configurable.

## License

MIT. See `LICENSE`.
