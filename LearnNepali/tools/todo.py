from pydantic_ai import Agent
from database.models import Todo
from database.session import get_session
from sqlalchemy import select
from datetime import datetime


def register_todo_tools(agent: Agent):

    @agent.tool_plain
    def create_todo(task: str, due_date: str) -> str:
        """Create a todo task. Only call after user explicitly confirms."""
        session = get_session()
        try:
            todo = Todo(task=task, due_date=datetime.fromisoformat(due_date), status="pending")
            session.add(todo)
            session.commit()
            return f"Todo created with ID: {todo.id}"
        finally:
            session.close()
    
    @agent.tool_plain
    def list_todos(status: str = None) -> str:
        """List all todos, optionally filtered by status."""
        session = get_session()
        try:
            query = select(Todo)
            if status:
                query = query.where(Todo.status == status)
            todos = session.execute(query).scalars().all()
            if not todos:
                return "No todos found."
            return "\n".join([f"{todo.id}: {todo.task} (Due: {todo.due_date}, Status: {todo.status})" for todo in todos])
        finally:
            session.close()
    
    @agent.tool_plain
    def update_status(todo_id: int, new_status: str) -> str:
        """Update the status of a todo."""
        session = get_session()
        try:
            todo = session.get(Todo, todo_id)
            if not todo:
                return f"Todo with ID {todo_id} not found."
            todo.status = new_status
            session.commit()
            return f"Todo ID {todo_id} status updated to {new_status}."
        finally:
            session.close()

    @agent.tool_plain
    def delete_todo(todo_id: int) -> str:
        """Delete a todo by ID."""
        session = get_session()
        try:
            todo = session.get(Todo, todo_id)
            if not todo:
                return f"Todo with ID {todo_id} not found."
            session.delete(todo)
            session.commit()
            return f"Todo ID {todo_id} deleted."
        finally:
            session.close()
    
    @agent.tool_plain
    def get_todo(todo_id: int) -> str:
        """Get details of a specific todo by ID."""
        session = get_session()
        try:
            todo = session.get(Todo, todo_id)
            if not todo:
                return f"Todo with ID {todo_id} not found."
            return f"{todo.id}: {todo.task} (Due: {todo.due_date}, Status: {todo.status})"
        finally:
            session.close()
