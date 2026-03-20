from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional

from pystonk import configuration


def _normalize_symbol(symbol: str) -> str:
    normalized = symbol.strip().upper()
    if not normalized:
        raise ValueError("Symbol is required.")
    return normalized


def _serialize_watchlist_row(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "symbol": row["symbol"],
        "note": row["note"],
        "created_at": row["created_at"],
    }


def _serialize_preset_row(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "symbol": row["symbol"],
        "history_percent": row["history_percent"],
        "history_frequency": row["history_frequency"],
        "history_period": row["history_period"],
        "history_start_to_end": bool(row["history_start_to_end"]),
        "options_target": row["options_target"],
        "options_expiration": row["options_expiration"],
        "options_use_percent": bool(row["options_use_percent"]),
        "created_at": row["created_at"],
    }


class WorkspaceStore:
    def __init__(self, db_path: str):
        self._db_path = Path(db_path).expanduser()
        if str(self._db_path) != ":memory:":
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @classmethod
    def from_configuration(cls) -> "WorkspaceStore":
        return cls(configuration["web"]["db_path"])

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(str(self._db_path))
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS watchlist (
                    symbol TEXT PRIMARY KEY,
                    note TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS presets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    history_percent REAL NOT NULL,
                    history_frequency TEXT NOT NULL,
                    history_period INTEGER NOT NULL,
                    history_start_to_end INTEGER NOT NULL DEFAULT 0,
                    options_target REAL NOT NULL,
                    options_expiration TEXT NOT NULL,
                    options_use_percent INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def list_watchlist(self) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT symbol, note, created_at
                FROM watchlist
                ORDER BY symbol ASC
                """
            ).fetchall()
        return [_serialize_watchlist_row(row) for row in rows]

    def get_watchlist_entry(self, symbol: str) -> Optional[Dict[str, Any]]:
        normalized_symbol = _normalize_symbol(symbol)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT symbol, note, created_at
                FROM watchlist
                WHERE symbol = ?
                """,
                (normalized_symbol,),
            ).fetchone()
        return _serialize_watchlist_row(row) if row else None

    def add_watchlist(self, symbol: str, note: str = "") -> Dict[str, Any]:
        normalized_symbol = _normalize_symbol(symbol)
        normalized_note = note.strip()

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO watchlist(symbol, note)
                VALUES(?, ?)
                ON CONFLICT(symbol)
                DO UPDATE SET note = excluded.note
                """,
                (normalized_symbol, normalized_note),
            )
            row = connection.execute(
                """
                SELECT symbol, note, created_at
                FROM watchlist
                WHERE symbol = ?
                """,
                (normalized_symbol,),
            ).fetchone()
        return _serialize_watchlist_row(row)

    def remove_watchlist(self, symbol: str) -> bool:
        normalized_symbol = _normalize_symbol(symbol)

        with self._connect() as connection:
            result = connection.execute(
                """
                DELETE FROM watchlist
                WHERE symbol = ?
                """,
                (normalized_symbol,),
            )
        return result.rowcount > 0

    def list_presets(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT id, name, symbol, history_percent, history_frequency, history_period,
                   history_start_to_end, options_target, options_expiration, options_use_percent,
                   created_at
            FROM presets
        """
        parameters = ()
        if symbol:
            query += " WHERE symbol = ?"
            parameters = (_normalize_symbol(symbol),)
        query += " ORDER BY created_at DESC, id DESC"

        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [_serialize_preset_row(row) for row in rows]

    def save_preset(
        self,
        name: str,
        symbol: str,
        history_percent: float,
        history_frequency: str,
        history_period: int,
        history_start_to_end: bool,
        options_target: float,
        options_expiration: str,
        options_use_percent: bool,
    ) -> Dict[str, Any]:
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Preset name is required.")

        normalized_symbol = _normalize_symbol(symbol)

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO presets(
                    name, symbol, history_percent, history_frequency, history_period,
                    history_start_to_end, options_target, options_expiration, options_use_percent
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    normalized_name,
                    normalized_symbol,
                    round(history_percent, 2),
                    history_frequency.strip().lower(),
                    int(history_period),
                    int(history_start_to_end),
                    round(options_target, 2),
                    options_expiration.strip().lower(),
                    int(options_use_percent),
                ),
            )
            row = connection.execute(
                """
                SELECT id, name, symbol, history_percent, history_frequency, history_period,
                       history_start_to_end, options_target, options_expiration, options_use_percent,
                       created_at
                FROM presets
                WHERE id = ?
                """,
                (cursor.lastrowid,),
            ).fetchone()
        return _serialize_preset_row(row)
