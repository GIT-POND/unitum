from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

'''
    #       Pydantic Overview       
    --------------------------
    - Data validation and settings management using python type annotations.
    - Pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
    - Define how data should be in pure, canonical python; validate it with pydantic.
'''
class Example(BaseModel):
    name: str
    quantity: int
    price: float
    delivered: datetime.date
    provider: EmailStr
    on_Sale: Optional[bool] = None  # {None} is the default value


#       User_Authentication        
class CreateUserAcc(BaseModel):
    username:str
    first_name:str
    last_name:str
    email:EmailStr
    password:str

class LoginUserAcc(BaseModel):
    email:EmailStr
    password:str

#       User_Account       
class UpdateUserAcc(BaseModel):
    username: str
    password: str


#       Check Username      
class CheckUsername(BaseModel):
    username: str


#       Task_List           
class CreateTaskList(BaseModel):
    list_name:str

class UpdateTaskList(BaseModel):
    list_name: str



#           Task            
class CreateTask(BaseModel):
    task_name:str
    task_note: Optional[str] = None
    deadline: Optional[datetime.date] = None

class UpdateTask(BaseModel):
    task_name: str
    task_note: Optional[str] = None
    deadline: Optional[datetime.date] = None

class CompleteTask(BaseModel):
    completed: bool



#           Responses       
class UserAccResponse(BaseModel):
    id: int
    username: str
    created_on: datetime.date

    class Config:
        orm_mode = True


class TaskListResponse(BaseModel):
    list_id: int
    list_name: str
    created_on: datetime.date
    creator_id:int

    class Config:
        orm_mode = True


class TaskResponse(BaseModel):
    task_id: int
    task_name: str
    created_on: datetime.date
    task_note: Optional[str] = None
    deadline: Optional[datetime.date] = None

    class Config:
        orm_mode = True


class CheckResponse(BaseModel):
    available: bool

    class Config:
        orm_mode = True
