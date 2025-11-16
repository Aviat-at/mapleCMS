"""Minimal aiosqlite implementation for local testing."""

from __future__ import annotations

import asyncio
import sqlite3
from functools import partial
from typing import Any, Iterable, Optional, Sequence

# Re-export the exception hierarchy expected from sqlite DB-API modules so
# SQLAlchemy's async driver can interact with this lightweight implementation.
for _exc_name in [
    "Error",
    "Warning",
    "InterfaceError",
    "DatabaseError",
    "OperationalError",
    "ProgrammingError",
    "IntegrityError",
    "DataError",
    "NotSupportedError",
]:
    globals()[_exc_name] = getattr(sqlite3, _exc_name)

__all__ = ["connect", "Connection", "Cursor"]

apilevel = "2.0"
threadsafety = 1
paramstyle = "qmark"
sqlite_version = sqlite3.sqlite_version
sqlite_version_info = sqlite3.sqlite_version_info
version = sqlite3.version
version_info = sqlite3.version_info


async def _run_in_thread(fn, *args, **kwargs):
    return await asyncio.to_thread(fn, *args, **kwargs)


class _ConnectionHandle:
    """Awaitable handle mimicking aiosqlite's thread wrapper."""

    def __init__(self, coro):
        self._coro = coro
        self.daemon = False

    def __await__(self):
        return self._coro.__await__()


class Cursor:
    """Simple async cursor wrapper."""

    def __init__(self, cursor: sqlite3.Cursor):
        self._cursor = cursor

    @property
    def rowcount(self) -> int:
        return self._cursor.rowcount

    @property
    def lastrowid(self) -> int:
        return self._cursor.lastrowid

    @property
    def description(self):
        return self._cursor.description

    async def execute(self, sql: str, parameters: Optional[Sequence[Any]] = None):
        await _run_in_thread(self._cursor.execute, sql, parameters or ())
        return self

    async def executemany(self, sql: str, seq_of_parameters: Iterable[Sequence[Any]]):
        await _run_in_thread(self._cursor.executemany, sql, seq_of_parameters)
        return self

    async def fetchone(self):
        return await _run_in_thread(self._cursor.fetchone)

    async def fetchmany(self, size: Optional[int] = None):
        if size is None:
            return await _run_in_thread(self._cursor.fetchmany)
        return await _run_in_thread(self._cursor.fetchmany, size)

    async def fetchall(self):
        return await _run_in_thread(self._cursor.fetchall)

    async def close(self):
        await _run_in_thread(self._cursor.close)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()


class Connection:
    """Async wrapper over sqlite3 connection."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    @property
    def row_factory(self):
        return self._conn.row_factory

    @row_factory.setter
    def row_factory(self, value):
        self._conn.row_factory = value

    async def cursor(self) -> Cursor:
        cursor = await _run_in_thread(self._conn.cursor)
        return Cursor(cursor)

    async def execute(self, sql: str, parameters: Optional[Sequence[Any]] = None):
        cursor = await self.cursor()
        return await cursor.execute(sql, parameters or ())

    async def executemany(self, sql: str, seq_of_parameters: Iterable[Sequence[Any]]):
        cursor = await self.cursor()
        return await cursor.executemany(sql, seq_of_parameters)

    async def executescript(self, sql_script: str):
        return await _run_in_thread(self._conn.executescript, sql_script)

    async def commit(self):
        await _run_in_thread(self._conn.commit)

    async def rollback(self):
        await _run_in_thread(self._conn.rollback)

    async def create_function(self, *args, **kwargs):
        await _run_in_thread(self._conn.create_function, *args, **kwargs)

    async def create_aggregate(self, *args, **kwargs):
        await _run_in_thread(self._conn.create_aggregate, *args, **kwargs)

    async def create_collation(self, *args, **kwargs):
        await _run_in_thread(self._conn.create_collation, *args, **kwargs)

    async def close(self):
        await _run_in_thread(self._conn.close)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()


async def _connect(database: str, **kwargs) -> Connection:
    row_factory = kwargs.pop("row_factory", sqlite3.Row)
    conn = await _run_in_thread(partial(sqlite3.connect, database, **kwargs))
    conn.row_factory = row_factory
    return Connection(conn)


def connect(database: str, **kwargs):
    """Return awaitable connection handle (mirrors upstream aiosqlite API)."""

    return _ConnectionHandle(_connect(database, **kwargs))
