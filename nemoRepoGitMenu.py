#!/usr/bin/python3
"""nemo-repo-git-menu: git commands in Nemo's right click menu.

Entries appear on a folder that is inside a git repository, on the folder
itself and on the empty background of an open folder. Each one opens a
terminal in the repository root, runs the command and leaves the shell open
so the output stays readable.

Requires nemo-repo-core: https://github.com/dualfroz/nemo-repo-core
"""

import importlib.util
import os
import sys


def _ensureCoreOnPath():
    if importlib.util.find_spec("nemoRepoCore") is not None:
        return
    dataHome = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    dataDirs = (os.environ.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share").split(":")
    for base in [dataHome] + dataDirs:
        candidate = os.path.join(base, "nemo-repo-core")
        if os.path.isdir(os.path.join(candidate, "nemoRepoCore")):
            sys.path.insert(0, candidate)
            return


_ensureCoreOnPath()

import gi

gi.require_version("Nemo", "3.0")
from gi.repository import GObject, Nemo

from nemoRepoCore import (coreConfig, findEnclosingRepoRoot, gitBinary,
                          launchTerminal, localDirectoryPath, requireCore)

requireCore("0.1.0")

pluginDefaults = {
    "actions": {
        "git_status": True,
        "git_log": True,
        "git_fetch": True,
        "git_pull": True,
    },
}

coreConfig.registerDefaults(pluginDefaults)

gitActions = [
    ("git_status", "Git Status", "git status",
     "Show the working tree status in a terminal"),
    ("git_log", "Git Log", "git log --oneline --graph --decorate -30",
     "Show the last 30 commits as a graph in a terminal"),
    ("git_fetch", "Git Fetch", "git fetch --all --prune",
     "Fetch every remote and prune deleted branches"),
    ("git_pull", "Git Pull", "git pull",
     "Pull the current branch from its upstream"),
]


def _menuItem(key, label, command, tip, repoRoot):
    item = Nemo.MenuItem(name="NemoRepoGitMenu::%s" % key,
                         label="%s (terminal)" % label,
                         tip="%s, in %s" % (tip, repoRoot))
    item.connect("activate", lambda *arguments: launchTerminal(repoRoot, command))
    return item


class RepoGitMenuProvider(GObject.GObject, Nemo.MenuProvider,
                          Nemo.NameAndDescProvider):

    def _itemsFor(self, path):
        if not gitBinary:
            return []
        repoRoot = findEnclosingRepoRoot(path)
        if repoRoot is None:
            return []
        return [_menuItem(key, label, command, tip, repoRoot)
                for key, label, command, tip in gitActions
                if coreConfig.sectionFlag("actions", key, True)]

    def get_file_items(self, window, files):
        if len(files) != 1:
            return []
        path = localDirectoryPath(files[0])
        return self._itemsFor(path) if path else []

    def get_background_items(self, window, currentFolder):
        path = localDirectoryPath(currentFolder)
        return self._itemsFor(path) if path else []

    def get_name_and_desc(self):
        return ["nemo-repo-git-menu:::Right click git actions (status, log, fetch, pull)"]
