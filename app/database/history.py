"""Historial de adaptaciones almacenado en SQLite."""

import sqlite3
from datetime import datetime
from typing import Any

from app import config

DEFAULT_LIMIT = 10

_SCHEMA = """
CREATE TABLE IF NOT EXISTS adaptations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    offer_text TEXT NOT NULL,
    adapted_cv TEXT NOT NULL,
    match_score INTEGER NOT NULL,
    pdf_path TEXT NOT NULL,
    source TEXT NOT NULL
);
"""


def init_db() -> None:
    config.HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        conn.execute(_SCHEMA)
        if not _column_exists(conn, "source"):
            conn.execute(
                "ALTER TABLE adaptations ADD COLUMN source TEXT NOT NULL "
                "DEFAULT 'texto'"
            )
        conn.commit()


def save_adaptation(
    offer_text: str, adapted_cv: str, pdf_path: str, match_score: int, source: str
) -> int:
    created_at = datetime.now().isoformat(timespec="seconds")
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO adaptations "
            "(created_at, offer_text, adapted_cv, match_score, pdf_path, source) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (created_at, offer_text, adapted_cv, match_score, pdf_path, source),
        )
        conn.commit()
        return int(cursor.lastrowid)


def list_adaptations(limit: int = DEFAULT_LIMIT) -> list[dict[str, Any]]:
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, created_at, offer_text, match_score, pdf_path, source "
            "FROM adaptations ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_adaptation(adaptation_id: int) -> dict[str, Any] | None:
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT id, created_at, offer_text, adapted_cv, match_score, pdf_path, "
            "source FROM adaptations WHERE id = ?",
            (adaptation_id,),
        ).fetchone()
    return dict(row) if row else None


def delete_adaptation(adaptation_id: int) -> str | None:
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT pdf_path FROM adaptations WHERE id = ?", (adaptation_id,)
        ).fetchone()
        if row is None:
            return None
        conn.execute("DELETE FROM adaptations WHERE id = ?", (adaptation_id,))
        conn.commit()
        return row["pdf_path"]


def _column_exists(conn: sqlite3.Connection, column: str) -> bool:
    rows = conn.execute("PRAGMA table_info(adaptations)").fetchall()
    return any(row[1] == column for row in rows)


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(str(config.DB_PATH))
