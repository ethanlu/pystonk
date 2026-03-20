from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from pystonk.storage.workspace import WorkspaceStore


class WorkspaceStoreTest(TestCase):
    def testWatchlistEntriesAreNormalizedAndUpdatable(self):
        with TemporaryDirectory() as tmpdir:
            store = WorkspaceStore(str(Path(tmpdir) / "workspace.sqlite3"))

            store.add_watchlist("spy", "weekly put desk")
            store.add_watchlist("SPY", "updated note")

            entries = store.list_watchlist()

            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["symbol"], "SPY")
            self.assertEqual(entries[0]["note"], "updated note")
            self.assertTrue(store.remove_watchlist("spy"))
            self.assertEqual(store.list_watchlist(), [])

    def testPresetsPersistTypedWorkspaceSettings(self):
        with TemporaryDirectory() as tmpdir:
            store = WorkspaceStore(str(Path(tmpdir) / "workspace.sqlite3"))

            preset = store.save_preset(
                name="SPY week 1.00premium",
                symbol="spy",
                history_percent=3.0,
                history_frequency="weekly",
                history_period=1,
                history_start_to_end=True,
                options_target=1.0,
                options_expiration="week",
                options_use_percent=False,
            )

            presets = store.list_presets("SPY")

            self.assertEqual(len(presets), 1)
            self.assertEqual(preset["symbol"], "SPY")
            self.assertTrue(presets[0]["history_start_to_end"])
            self.assertFalse(presets[0]["options_use_percent"])
            self.assertEqual(presets[0]["name"], "SPY week 1.00premium")
