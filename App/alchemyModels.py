
from .database import Base

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Date
# from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



class Task(Base):
    __tablename__ = 'Task'

    task_id = Column(Integer, primary_key=True, nullable=False) # Primary Key
    task_name = Column(String, nullable=False)
    task_note = Column(String, nullable=True)
    completed = Column(Boolean, nullable=False, default=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'))
    deadline = Column(TIMESTAMP(timezone=True), nullable=True)
    list_id = Column(Integer, ForeignKey('Task_List.list_id', ondelete='CASCADE'), nullable=False)


class TaskList(Base):
    __tablename__ = 'Task_List'

    list_id = Column(Integer, primary_key=True, nullable=False) # Primary Key
    list_name = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'))
    creator_id = Column(Integer, ForeignKey('User_Account.id', ondelete='CASCADE'), nullable=False)
    creator= relationship('UserAcc')


class UserAcc(Base):
    __tablename__ = 'User_Account'

    id = Column(Integer, primary_key=True, nullable=False) #Primary Key
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'))