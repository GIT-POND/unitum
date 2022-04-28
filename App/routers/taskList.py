# http request libs
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
router = APIRouter(prefix='/list', tags=['list'])


#           CREATE LIST                 
@router.post('/create_list', status_code=status.HTTP_201_CREATED, response_model=pydanticModels.TaskListResponse)
def create_task_list(task_list:pydanticModels.CreateTaskList, db:Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: Create a new task list.
    @param task_list - the task list to create.
    @param db - the database session.
    @param user_id - the user id.
    @returns the new task list.
    """
    try:
        new_task_list = alchemyModels.TaskList(creator_id = user_id, **task_list.dict())
        
        #NOTE: if the list already exists, update it instead of creating a new one
        db.add(new_task_list)
        db.commit()
        db.refresh(new_task_list)

        return new_task_list
    except BaseException as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           READ USER LISTS         
@router.get('/view_lists', status_code=status.HTTP_200_OK, response_model=List[pydanticModels.TaskListResponse])
def view_task_lists(db: Session=Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: View all task lists for a user.
    @param db - the database session
    @param user_id - the user id
    @returns the task lists
    """
    try:
        #NOTE: if a search parameter is given, it searches for a specific list
        task_lists = db.query(alchemyModels.TaskList).filter(alchemyModels.TaskList.creator_id == user_id).all()
        
        return task_lists
    except BaseException as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           READ LISTS                 
@router.get('/view_list/{name}', status_code=status.HTTP_200_OK, response_model=List[pydanticModels.TaskListResponse])
def view_task_lists(name:str, db: Session=Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: View a list of tasks for a specific list.
    @param name - the name of the list you want to view.
    @param db - the database session.
    @param user_id - the user id of the user making the request.
    @returns the list of tasks for the list.
    """
    try:
        #NOTE: if a search parameter is given, it searches for a specific list
        task_lists = db.query(alchemyModels.TaskList).filter(alchemyModels.TaskList.list_name == name, alchemyModels.TaskList.creator_id == user_id).all()

        return task_lists
    except BaseException as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           UPDATE LIST                 
@router.put('/update_list/', status_code=status.HTTP_200_OK, response_model=pydanticModels.TaskListResponse)
def update_task_list(list_id:int, updated_list: pydanticModels.UpdateTaskList, db:Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: Update the task list with the new information.
    @param list_id - the id of the list to update.
    @param updated_list - the new information for the list.
    @param db - the database session.
    @param user_id - the user id of the user making the request.
    @returns the updated list.
    """
    try:
        container = db.query(alchemyModels.TaskList).filter(alchemyModels.TaskList.list_id == list_id, alchemyModels.TaskList.creator_id == user_id)
        list_in_container = container.first()

        #NOTE: If the container is empty, raise 404 exception
        if list_in_container is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        container.update(updated_list.dict(), synchronize_session=False)
        db.commit()

        return container.first()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

#           DELETE LIST                 
@router.delete('/delete_list/')
def delete_task_list(list_id:int, db:Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: Delete a task list from the database.
    @param list_id - the id of the list to delete
    @param db - the database session
    @param user_id - the user id of the user making the request
    @returns a 204 response if successful
    """
    try:
        container = db.query(alchemyModels.TaskList).filter(alchemyModels.TaskList.list_id == list_id, alchemyModels.TaskList.creator_id == user_id)

        #NOTE: if the container is empty, raise 404 exception
        if container.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        container.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
