from ast import Break
from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
# working with ORM
from sqlalchemy.orm import Session
from App.database import get_db
# working with other py files
from App import alchemyModels, pydanticModels
from App.auth import AuthHandler



auth_handler = AuthHandler()

#           ROUTER EXTENSION            
router = APIRouter(prefix='/task', tags=['task'])


#           CREATE TASK                 
@router.post('/create_task/', status_code=status.HTTP_201_CREATED, response_model=pydanticModels.TaskResponse)
def create_task(list_id:int, task:pydanticModels.CreateTask, db:Session=Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: Create a new task in the database.
    @param list_id - the list id of the task list the task is in.
    @param task - the task to be created.
    @param db - the database session.
    @param user_id - the user id of the user creating the task.
    @returns the new task.
    """
    try:
        #NOTE: verify JWT user owns the task list where the task will be created
        verified_list = db.query(alchemyModels.TaskList.creator_id == user_id, alchemyModels.TaskList.list_id == list_id).first()

        if verified_list:
            new_task = alchemyModels.Task(list_id = list_id, **task.dict())

            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            return new_task
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           READ TASKS                  
@router.get('/view_tasks/', status_code=status.HTTP_200_OK, response_model=List[pydanticModels.TaskResponse])
def view_tasks(list_id:int, db:Session=Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: View the tasks in a list.
    @param list_id - the list id
    @param db - the database session
    @param user_id - the user id
    @returns the tasks in the list
    """
    try:
        #NOTE: verify JWT user owns the task list where the task will be created
        verified_list = db.query(alchemyModels.TaskList.creator_id == user_id, alchemyModels.TaskList.list_id == list_id).first()

        if verified_list:
            tasks = db.query(alchemyModels.Task).filter(alchemyModels.Task.list_id == list_id).all()
            
            return tasks
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           UPDATE TASK                 
@router.put('/update_task/', status_code=status.HTTP_200_OK, response_model=pydanticModels.TaskResponse)
def update_task(task_id:int, updated_task:pydanticModels.UpdateTask, db:Session=Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: Update a task in the database.
    @param task_id - the task id to update
    @param updated_task - the updated task
    @param db - the database session
    @param user_id - the user id
    @returns the updated task
    """
    try:
        verified_task = db.query(alchemyModels.Task).filter(alchemyModels.Task.task_id == task_id).first()

        #NOTE: verify JWT user owns the task list where the task will be created
        verified_list = db.query(alchemyModels.TaskList.creator_id == user_id, alchemyModels.TaskList.list_id == verified_task.task_id).first()

        if verified_list:
            container = db.query(alchemyModels.Task).filter(alchemyModels.Task.task_id == task_id)
            task_in_container = container.first()
            
            container.update(updated_task.dict(), synchronize_session=False)
            db.commit()

            return container.first()
    except BaseException as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           DELETE TASK                 
@router.delete('/delete_task/')
def delete_task(task_id:int, db:Session=Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: Delete a task from the database.
    @param task_id - the task id to delete
    @param db - the database session
    @param user_id - the user id of the user who is deleting the task
    @returns a response with the status code 204 if successful
    """
    try:
        verified_task = db.query(alchemyModels.Task).filter(alchemyModels.Task.task_id == task_id).first()

        #NOTE: verify JWT user owns the task list where the task will be created
        verified_list = db.query(alchemyModels.TaskList.creator_id == user_id, alchemyModels.TaskList.list_id == verified_task.task_id).first()

        if verified_list:
            task = db.query(alchemyModels.Task).filter(alchemyModels.Task.task_id == task_id)
            
            task.delete(synchronize_session=False)
            db.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except BaseException as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
