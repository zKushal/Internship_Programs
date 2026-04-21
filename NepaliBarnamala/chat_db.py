import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from psycopg import connect


VALID_STATUSES = {"pending", "learning", "completed"}
TODO_TABLE = "todos"
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL was not found. Add it to your .env file or set it in your environment."
        )
    return database_url


def initialize_database() -> None:
    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id SERIAL PRIMARY KEY,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {TODO_TABLE} (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
            cursor.execute(
                f"""
                ALTER TABLE {TODO_TABLE}
                ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '',
                ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'pending',
                ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                """
            )
            cursor.execute(
                f"""
                ALTER TABLE {TODO_TABLE}
                ALTER COLUMN description SET DEFAULT '',
                ALTER COLUMN status SET DEFAULT 'pending',
                ALTER COLUMN created_at SET DEFAULT NOW(),
                ALTER COLUMN updated_at SET DEFAULT NOW()
                """
            )
            cursor.execute(
                f"""
                UPDATE {TODO_TABLE}
                SET description = COALESCE(description, ''),
                    status = COALESCE(NULLIF(TRIM(status), ''), 'pending'),
                    created_at = COALESCE(created_at, NOW()),
                    updated_at = COALESCE(updated_at, created_at, NOW())
                """
            )
            cursor.execute(
                f"""
                ALTER TABLE {TODO_TABLE}
                ALTER COLUMN description SET NOT NULL,
                ALTER COLUMN status SET NOT NULL,
                ALTER COLUMN created_at SET NOT NULL,
                ALTER COLUMN updated_at SET NOT NULL
                """
            )
            cursor.execute(
                """
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_schema = 'public' AND table_name = 'learning_todos'
                    ) THEN
                        INSERT INTO todos (title, description, status, created_at, updated_at)
                        SELECT lt.title, lt.description, lt.status, lt.created_at, lt.updated_at
                        FROM learning_todos lt
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM todos t
                            WHERE t.title = lt.title
                              AND t.description = lt.description
                              AND t.created_at = lt.created_at
                        );
                    END IF;
                END
                $$;
                """
            )
            cursor.execute(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'todos_status_check'
                    ) THEN
                        ALTER TABLE todos
                        ADD CONSTRAINT todos_status_check
                        CHECK (status IN ('pending', 'learning', 'completed'));
                    END IF;
                END
                $$;
                """
            )
        connection.commit()


def save_message(role: str, content: str) -> None:
    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO chat_messages (role, content)
                VALUES (%s, %s)
                """,
                (role, content),
            )
        connection.commit()


def get_recent_messages(limit: int = 10) -> list[tuple[str, str, Any]]:
    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT role, content, created_at
                FROM chat_messages
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cursor.fetchall()

    return list(reversed(rows))


def create_todos(tasks: list[dict[str, str]]) -> list[dict[str, Any]]:
    if not tasks:
        return []

    sanitized_tasks: list[tuple[str, str, str]] = []
    for index, task in enumerate(tasks):
        title = task.get("title", "").strip()
        description = task.get("description", "").strip()
        status = task.get("status", "pending").strip().lower() or "pending"

        if not title:
            continue

        if not description:
            description = "No description provided."

        if status not in VALID_STATUSES:
            status = "learning" if index == 0 else "pending"

        sanitized_tasks.append((title, description, status))

    if not sanitized_tasks:
        return []

    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                f"""
                INSERT INTO {TODO_TABLE} (title, description, status)
                VALUES (%s, %s, %s)
                """,
                sanitized_tasks,
            )
            cursor.execute(
                f"""
                SELECT id, title, description, status, created_at, updated_at
                FROM {TODO_TABLE}
                ORDER BY id DESC
                LIMIT %s
                """,
                (len(sanitized_tasks),),
            )
            rows = list(reversed(cursor.fetchall()))
        connection.commit()

    return [_row_to_todo(row) for row in rows]


def list_todos(status: str = "all") -> list[dict[str, Any]]:
    normalized_status = status.lower().strip()

    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            if normalized_status == "all":
                cursor.execute(
                    f"""
                    SELECT id, title, description, status, created_at, updated_at
                    FROM {TODO_TABLE}
                    ORDER BY id
                    """
                )
            else:
                cursor.execute(
                    f"""
                    SELECT id, title, description, status, created_at, updated_at
                    FROM {TODO_TABLE}
                    WHERE status = %s
                    ORDER BY id
                    """,
                    (normalized_status,),
                )
            rows = cursor.fetchall()

    return [_row_to_todo(row) for row in rows]


def search_todos(query: str) -> list[dict[str, Any]]:
    trimmed_query = query.strip()
    if not trimmed_query:
        return []

    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            if trimmed_query.isdigit():
                cursor.execute(
                    f"""
                    SELECT id, title, description, status, created_at, updated_at
                    FROM {TODO_TABLE}
                    WHERE id = %s
                    ORDER BY id
                    """,
                    (int(trimmed_query),),
                )
            else:
                pattern = f"%{trimmed_query}%"
                cursor.execute(
                    f"""
                    SELECT id, title, description, status, created_at, updated_at
                    FROM {TODO_TABLE}
                    WHERE title ILIKE %s OR description ILIKE %s OR status ILIKE %s
                    ORDER BY id
                    """,
                    (pattern, pattern, pattern),
                )
            rows = cursor.fetchall()

    return [_row_to_todo(row) for row in rows]


def update_todo_status(todo_id: int, status: str) -> dict[str, Any] | None:
    normalized_status = status.lower().strip()
    if normalized_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE {TODO_TABLE}
                SET status = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING id, title, description, status, created_at, updated_at
                """,
                (normalized_status, todo_id),
            )
            row = cursor.fetchone()

            if row and normalized_status == "completed":
                cursor.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM {TODO_TABLE}
                    WHERE status = 'learning'
                    """
                )
                learning_count = cursor.fetchone()[0]
                if learning_count == 0:
                    cursor.execute(
                        f"""
                        UPDATE {TODO_TABLE}
                        SET status = 'learning', updated_at = NOW()
                        WHERE id = (
                            SELECT id
                            FROM {TODO_TABLE}
                            WHERE status = 'pending'
                            ORDER BY id
                            LIMIT 1
                        )
                        RETURNING id, title, description, status, created_at, updated_at
                        """
                    )
            connection.commit()

    return _row_to_todo(row) if row else None


def delete_todo(todo_id: int) -> dict[str, Any] | None:
    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                DELETE FROM {TODO_TABLE}
                WHERE id = %s
                RETURNING id, title, description, status, created_at, updated_at
                """,
                (todo_id,),
            )
            row = cursor.fetchone()
        connection.commit()

    return _row_to_todo(row) if row else None


def get_last_learned(limit: int = 5) -> list[tuple[str, Any]]:
    with connect(get_database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT content, created_at
                FROM chat_messages
                WHERE role = 'assistant'
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cursor.fetchall()

    return list(reversed(rows))


def _row_to_todo(row: Any) -> dict[str, Any]:
    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "status": row[3],
        "created_at": row[4],
        "updated_at": row[5],
    }
