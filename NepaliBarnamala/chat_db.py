import os
from psycopg import connect

VALID_STATUSES = {"pending", "learning", "completed"}


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL not found")
    return database_url


# =========================
# CHAT MESSAGES
# =========================
def save_message(role: str, content: str) -> None:
    with connect(get_database_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO chat_messages (role, content) VALUES (%s, %s)",
                (role, content),
            )
        conn.commit()


def get_recent_messages(limit: int = 10):
    with connect(get_database_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT role, content, created_at
                FROM chat_messages
                ORDER BY id ASC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()


# =========================
# TODO OPERATIONS
# =========================
def create_todos(tasks: list[dict]):
    results = []

    with connect(get_database_url()) as conn:
        with conn.cursor() as cur:
            for task in tasks:
                cur.execute(
                    """
                    INSERT INTO learning_todos (title, description, status)
                    VALUES (%s, %s, %s)
                    RETURNING id, title, description, status
                    """,
                    (
                        task["title"],
                        task.get("description", ""),
                        task.get("status", "pending"),
                    ),
                )
                results.append(cur.fetchone())

        conn.commit()

    return results


def list_todos(status="all"):
    with connect(get_database_url()) as conn:
        with conn.cursor() as cur:

            if status == "all":
                cur.execute("SELECT id, title, description, status FROM learning_todos")
            else:
                cur.execute(
                    "SELECT id, title, description, status FROM learning_todos WHERE status=%s",
                    (status,),
                )

            return cur.fetchall()


def update_todo_status(todo_id, status):
    with connect(get_database_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE learning_todos 
                SET status=%s, updated_at=NOW() 
                WHERE id=%s
                RETURNING id, status
                """,
                (status, todo_id),
            )
            row = cur.fetchone()
        conn.commit()

    return row


def delete_todo(todo_id):
    with connect(get_database_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM learning_todos WHERE id=%s RETURNING id",
                (todo_id,),
            )
            row = cur.fetchone()
        conn.commit()

    return row


def search_todos(query):
    with connect(get_database_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, status
                FROM learning_todos
                WHERE title ILIKE %s OR description ILIKE %s
                """,
                (f"%{query}%", f"%{query}%"),
            )
            return cur.fetchall()