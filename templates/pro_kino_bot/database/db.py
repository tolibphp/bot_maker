"""Async SQLite database kino bot uchun."""

from __future__ import annotations

from pathlib import Path

import aiosqlite


class Database:
    """Kino bot ma'lumotlar bazasi."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)
        self.db: aiosqlite.Connection | None = None

    # ── Ulanish ─────────────────────────────────────

    async def connect(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db = await aiosqlite.connect(self.db_path)
        self.db.row_factory = aiosqlite.Row
        await self._create_tables()

    async def close(self) -> None:
        if self.db:
            await self.db.close()

    async def _create_tables(self) -> None:
        await self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER UNIQUE NOT NULL,
                full_name   TEXT,
                username    TEXT,
                joined_at   TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS movies (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                code        TEXT UNIQUE NOT NULL,
                title       TEXT NOT NULL,
                file_id     TEXT NOT NULL,
                file_type   TEXT DEFAULT 'video',
                caption     TEXT,
                views       INTEGER DEFAULT 0,
                added_by    INTEGER,
                added_at    TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS channels (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id       INTEGER UNIQUE NOT NULL,
                channel_username TEXT,
                channel_title    TEXT,
                invite_link      TEXT,
                added_at         TEXT DEFAULT (datetime('now'))
            );
            """
        )
        
        # Migration for invite_link
        try:
            await self.db.execute("ALTER TABLE channels ADD COLUMN invite_link TEXT")
        except Exception:
            pass
            
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS join_requests (
                user_id INTEGER,
                channel_id INTEGER,
                requested_at TEXT DEFAULT (datetime('now')),
                PRIMARY KEY (user_id, channel_id)
            )
            """
        )
        await self.db.commit()

    # ── Foydalanuvchilar ────────────────────────────

    async def add_user(
        self, user_id: int, full_name: str, username: str | None
    ) -> bool:
        try:
            await self.db.execute(
                "INSERT OR IGNORE INTO users (user_id, full_name, username) "
                "VALUES (?, ?, ?)",
                (user_id, full_name, username),
            )
            await self.db.commit()
            return True
        except Exception:
            return False

    async def get_user(self, user_id: int) -> aiosqlite.Row | None:
        async with self.db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone()

    async def get_all_user_ids(self) -> list[int]:
        async with self.db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def get_user_count(self) -> int:
        async with self.db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0]

    # ── Kinolar ─────────────────────────────────────

    async def add_movie(
        self,
        code: str,
        title: str,
        file_id: str,
        file_type: str = "video",
        caption: str | None = None,
        added_by: int | None = None,
    ) -> bool:
        try:
            await self.db.execute(
                "INSERT INTO movies "
                "(code, title, file_id, file_type, caption, added_by) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (code, title, file_id, file_type, caption, added_by),
            )
            await self.db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False

    async def get_movie_by_code(self, code: str) -> aiosqlite.Row | None:
        async with self.db.execute(
            "SELECT * FROM movies WHERE code = ?", (code,)
        ) as cursor:
            return await cursor.fetchone()

    async def search_movies(
        self, query: str, limit: int = 50
    ) -> list[aiosqlite.Row]:
        async with self.db.execute(
            "SELECT * FROM movies WHERE title LIKE ? OR code LIKE ? "
            "ORDER BY views DESC LIMIT ?",
            (f"%{query}%", f"%{query}%", limit),
        ) as cursor:
            return await cursor.fetchall()

    async def get_popular_movies(
        self, limit: int = 10
    ) -> list[aiosqlite.Row]:
        async with self.db.execute(
            "SELECT * FROM movies ORDER BY views DESC LIMIT ?", (limit,)
        ) as cursor:
            return await cursor.fetchall()

    async def get_recent_movies(
        self, limit: int = 10
    ) -> list[aiosqlite.Row]:
        async with self.db.execute(
            "SELECT * FROM movies ORDER BY added_at DESC LIMIT ?", (limit,)
        ) as cursor:
            return await cursor.fetchall()

    async def get_all_movies(
        self, offset: int = 0, limit: int = 50
    ) -> list[aiosqlite.Row]:
        async with self.db.execute(
            "SELECT * FROM movies ORDER BY added_at DESC "
            "LIMIT ? OFFSET ?",
            (limit, offset),
        ) as cursor:
            return await cursor.fetchall()

    async def delete_movie(self, code: str) -> bool:
        cursor = await self.db.execute(
            "DELETE FROM movies WHERE code = ?", (code,)
        )
        await self.db.commit()
        return cursor.rowcount > 0

    async def get_movie_count(self) -> int:
        async with self.db.execute("SELECT COUNT(*) FROM movies") as cursor:
            row = await cursor.fetchone()
            return row[0]

    async def increment_views(self, code: str) -> None:
        await self.db.execute(
            "UPDATE movies SET views = views + 1 WHERE code = ?", (code,)
        )
        await self.db.commit()

    async def get_total_views(self) -> int:
        async with self.db.execute(
            "SELECT COALESCE(SUM(views), 0) FROM movies"
        ) as cursor:
            row = await cursor.fetchone()
            return row[0]

    # ── Kanallar ────────────────────────────────────

    async def add_channel(
        self,
        channel_id: int,
        channel_username: str | None,
        channel_title: str | None,
        invite_link: str | None = None
    ) -> bool:
        try:
            await self.db.execute(
                "INSERT OR REPLACE INTO channels "
                "(channel_id, channel_username, channel_title, invite_link) "
                "VALUES (?, ?, ?, ?)",
                (channel_id, channel_username, channel_title, invite_link),
            )
            await self.db.commit()
            return True
        except Exception:
            return False

    async def get_channels(self) -> list[aiosqlite.Row]:
        async with self.db.execute("SELECT * FROM channels") as cursor:
            return await cursor.fetchall()

    async def add_join_request(self, user_id: int, channel_id: int) -> None:
        await self.db.execute(
            "INSERT OR IGNORE INTO join_requests (user_id, channel_id) VALUES (?, ?)",
            (user_id, channel_id)
        )
        await self.db.commit()

    async def has_join_request(self, user_id: int, channel_id: int) -> bool:
        async with self.db.execute(
            "SELECT 1 FROM join_requests WHERE user_id = ? AND channel_id = ?",
            (user_id, channel_id)
        ) as cursor:
            row = await cursor.fetchone()
            return row is not None

    async def remove_channel(self, channel_id: int) -> bool:
        cursor = await self.db.execute(
            "DELETE FROM channels WHERE channel_id = ?", (channel_id,)
        )
        await self.db.commit()
        return cursor.rowcount > 0

    # ── Statistika ──────────────────────────────────

    async def get_today_users(self) -> int:
        async with self.db.execute(
            "SELECT COUNT(*) FROM users "
            "WHERE DATE(joined_at) = DATE('now')"
        ) as cursor:
            row = await cursor.fetchone()
            return row[0]
