from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")

    def __repr__(self):
        return f"<Todo(id={self.id}, task='{self.task}', due_date='{self.due_date}', status='{self.status}')>"