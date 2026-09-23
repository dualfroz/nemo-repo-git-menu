import os
import unittest
from unittest import mock

import support
from support import (FakeNemoFile, makeDirectory, makeFakeRepository,
                     resetSharedState, writeConfig, writeFile)

plugin = support.importPlugin("nemoRepoGitMenu")

from nemoRepoCore import coreConfig

expectedEntries = [
    ("git_status", "Git Status (terminal)", "git status"),
    ("git_log", "Git Log (terminal)", "git log --oneline --graph --decorate -30"),
    ("git_fetch", "Git Fetch (terminal)", "git fetch --all --prune"),
    ("git_pull", "Git Pull (terminal)", "git pull"),
]


class GitMenuTestCase(unittest.TestCase):

    def setUp(self):
        resetSharedState()
        self.addCleanup(resetSharedState)
        gitPatch = mock.patch.object(plugin, "gitBinary", "/usr/bin/git")
        launchPatch = mock.patch.object(plugin, "launchTerminal")
        gitPatch.start()
        self.launchTerminal = launchPatch.start()
        self.addCleanup(gitPatch.stop)
        self.addCleanup(launchPatch.stop)
        self.provider = plugin.RepoGitMenuProvider()
        self.repository = makeFakeRepository()

    def names(self, items):
        return [item.props.name for item in items]


class EntryTests(GitMenuTestCase):

    def testAllEntriesOnRepositoryRoot(self):
        items = self.provider._itemsFor(self.repository)
        self.assertEqual(self.names(items),
                         ["NemoRepoGitMenu::%s" % key for key, _, _ in expectedEntries])
        self.assertEqual([item.props.label for item in items],
                         [label for _, label, _ in expectedEntries])

    def testTipNamesRepositoryRoot(self):
        for item in self.provider._itemsFor(self.repository):
            self.assertTrue(item.props.tip.endswith(", in %s" % self.repository))

    def testActivationRunsCommandInRepositoryRoot(self):
        nested = os.path.join(self.repository, "src", "deep")
        os.makedirs(nested)
        for item, (key, _, command) in zip(self.provider._itemsFor(nested), expectedEntries):
            with self.subTest(entry=key):
                self.launchTerminal.reset_mock()
                item.activate()
                self.launchTerminal.assert_called_once_with(self.repository, command)

    def testEntriesAppearInsideRepository(self):
        nested = os.path.join(self.repository, "src")
        os.mkdir(nested)
        self.assertEqual(len(self.provider._itemsFor(nested)), 4)

    def testNothingOutsideRepository(self):
        self.assertEqual(self.provider._itemsFor(makeDirectory()), [])

    def testNothingWithoutGit(self):
        with mock.patch.object(plugin, "gitBinary", None):
            self.assertEqual(self.provider._itemsFor(self.repository), [])

    def testEntryCanBeSwitchedOff(self):
        writeConfig(coreConfig, {"actions": {"git_fetch": False}})
        self.assertEqual(self.names(self.provider._itemsFor(self.repository)), [
            "NemoRepoGitMenu::git_status", "NemoRepoGitMenu::git_log",
            "NemoRepoGitMenu::git_pull"])

    def testEnabledObjectFormIsAccepted(self):
        writeConfig(coreConfig, {"actions": {"git_log": {"enabled": False}}})
        self.assertNotIn("NemoRepoGitMenu::git_log",
                         self.names(self.provider._itemsFor(self.repository)))

    def testAllEntriesOff(self):
        writeConfig(coreConfig, {"actions": {key: False for key, _, _ in expectedEntries}})
        self.assertEqual(self.provider._itemsFor(self.repository), [])

    def testDefaultsRegistered(self):
        for key, _, _ in expectedEntries:
            self.assertTrue(coreConfig.section("actions")[key])


class SelectionTests(GitMenuTestCase):

    def testSingleFolder(self):
        items = self.provider.get_file_items(None, [FakeNemoFile(self.repository)])
        self.assertEqual(len(items), 4)

    def testSeveralFolders(self):
        files = [FakeNemoFile(self.repository), FakeNemoFile(self.repository)]
        self.assertEqual(self.provider.get_file_items(None, files), [])

    def testRegularFile(self):
        path = writeFile(self.repository, "file.txt")
        files = [FakeNemoFile(path, isDirectory=False)]
        self.assertEqual(self.provider.get_file_items(None, files), [])

    def testRemoteFolder(self):
        files = [FakeNemoFile(self.repository, scheme="sftp")]
        self.assertEqual(self.provider.get_file_items(None, files), [])

    def testBackground(self):
        items = self.provider.get_background_items(None, FakeNemoFile(self.repository))
        self.assertEqual(len(items), 4)

    def testRemoteBackground(self):
        folder = FakeNemoFile(self.repository, scheme="smb")
        self.assertEqual(self.provider.get_background_items(None, folder), [])

    def testNameAndDescription(self):
        [entry] = self.provider.get_name_and_desc()
        self.assertTrue(entry.startswith("nemo-repo-git-menu:::"))


if __name__ == "__main__":
    unittest.main()
