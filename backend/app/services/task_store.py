"""
SQLite-backed task store for persistent task state.
Replaces the in-memory dict used by TaskManager so that task state
survives server restarts.
"""

import json
import os
import sqlite3
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id          TEXT PRIMARY KEY,
    task_type   TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending',
    progress    REAL NOT NULL DEFAULT 0,
    message     TEXT NOT NULL DEFAULT '',
    result      TEXT,
    error       TEXT,
    metadata    TEXT,
    progress_detail TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
)
"""


class SQLiteTaskStore:
    """Thread-safe SQLite storage that mirrors the TaskManager interface."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), '..', '..', 'uploads', 'tasks.db'
            )
        self._db_path = os.path.abspath(db_path)

        # Ensure the parent directory exists
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)

        self._write_lock = threading.Lock()
        self._init_db()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_conn(self) -> sqlite3.Connection:
        """Return a per-thread connection with WAL mode."""
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        with self._write_lock:
            conn = self._get_conn()
            try:
                conn.execute(_CREATE_TABLE)
                # Mark any incomplete tasks from a previous run as interrupted
                conn.execute(
                    "UPDATE tasks SET status = 'interrupted', "
                    "message = 'Server restarted', updated_at = ? "
                    "WHERE status IN ('pending', 'processing')",
                    (datetime.now().isoformat(),),
                )
                conn.commit()
            finally:
                conn.close()

    @staticmethod
    def _serialize(obj: Any) -> Optional[str]:
        if obj is None:
            return None
        return json.dumps(obj, ensure_ascii=False)

    @staticmethod
    def _deserialize(text: Optional[str]) -> Any:
        if text is None:
            return None
        return json.loads(text)

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "task_id": row["id"],
            "task_type": row["task_type"],
            "status": row["status"],
            "progress": row["progress"],
            "message": row["message"],
            "result": self._deserialize(row["result"]),
            "error": row["error"],
            "metadata": self._deserialize(row["metadata"]) or {},
            "progress_detail": self._deserialize(row["progress_detail"]) or {},
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    # ------------------------------------------------------------------
    # Public API (mirrors TaskManager)
    # ------------------------------------------------------------------

    def create_task(self, task_id: str, task_type: str,
                    metadata: Optional[Dict] = None) -> str:
        now = datetime.now().isoformat()
        with self._write_lock:
            conn = self._get_conn()
            try:
                conn.execute(
                    "INSERT INTO tasks (id, task_type, status, progress, message, "
                    "metadata, progress_detail, created_at, updated_at) "
                    "VALUES (?, ?, 'pending', 0, '', ?, '{}', ?, ?)",
                    (task_id, task_type, self._serialize(metadata or {}), now, now),
                )
                conn.commit()
            finally:
                conn.close()
        return task_id

    def update_task(self, task_id: str, **kwargs) -> None:
        """
        Accepted kwargs: status, progress, message, result, error,
        metadata, progress_detail.
        """
        if not kwargs:
            return

        columns: List[str] = []
        values: List[Any] = []

        json_fields = {"result", "metadata", "progress_detail"}
        for key, val in kwargs.items():
            if val is None:
                continue
            if key in json_fields:
                columns.append(f"{key} = ?")
                values.append(self._serialize(val))
            else:
                columns.append(f"{key} = ?")
                values.append(val)

        if not columns:
            return

        columns.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(task_id)

        sql = f"UPDATE tasks SET {', '.join(columns)} WHERE id = ?"

        with self._write_lock:
            conn = self._get_conn()
            try:
                conn.execute(sql, values)
                conn.commit()
            finally:
                conn.close()

    def complete_task(self, task_id: str, result: Dict) -> None:
        self.update_task(
            task_id,
            status="completed",
            progress=100,
            message="任务完成",
            result=result,
        )

    def fail_task(self, task_id: str, error: str) -> None:
        self.update_task(
            task_id,
            status="failed",
            message="任务失败",
            error=error,
        )

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            if row is None:
                return None
            return self._row_to_dict(row)
        finally:
            conn.close()

    def get_all_tasks(self, task_type: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        try:
            if task_type:
                rows = conn.execute(
                    "SELECT * FROM tasks WHERE task_type = ? ORDER BY created_at DESC",
                    (task_type,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM tasks ORDER BY created_at DESC"
                ).fetchall()
            return [self._row_to_dict(r) for r in rows]
        finally:
            conn.close()

    def cleanup_old_tasks(self, max_age_hours: int = 24) -> None:
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(hours=max_age_hours)).isoformat()
        with self._write_lock:
            conn = self._get_conn()
            try:
                conn.execute(
                    "DELETE FROM tasks WHERE created_at < ? "
                    "AND status IN ('completed', 'failed', 'interrupted')",
                    (cutoff,),
                )
                conn.commit()
            finally:
                conn.close()
