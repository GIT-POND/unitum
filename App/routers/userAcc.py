# http request libs
from fastapi import Response, status, HTTPException, Depends, APIRouter
# working with ORM
from sqlalchemy.orm import Session
from App.database import get_db
# working with other py files
from App import alchemyModels, pydanticModels
from App.auth import AuthHandler



auth_handler = AuthHandler()

#           ROUTER EXTENSION            
router = APIRouter(prefix='/user', tags=['user'])


#           READ ACCOUNT                
@router.get('/view_account', status_code=status.HTTP_200_OK, response_model=pydanticModels.UserAccResponse)
def view_user_account( db:Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: View the user account belonging to the user.
    @param db - the database session           
    @param user_id - the user id           
    @return The user account for the user.           
    """
    try:
        user_account = db.query(alchemyModels.UserAcc).filter(alchemyModels.UserAcc.id == user_id).first()

        #NOTE: If user account doesn't exist, return 404
        if user_account is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        return user_account
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           UPDATE ACCOUNT              
@router.put('/update_account', status_code=status.HTTP_200_OK, response_model=pydanticModels.UserAccResponse) 
def update_user_account(updated_account:pydanticModels.UpdateUserAcc, db:Session=Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: Update the user account with the new information.
    @param updated_account - the new information for the account           
    @param db - the database session           
    @param user_id - the user id           
    @return The updated account           
    """
    try:
        container = db.query(alchemyModels.UserAcc).filter(alchemyModels.UserAcc.id == user_id)
        account_in_container = container.first()

        #NOTE: if the account is in the container, return the account itself, otherwise raise exception
        if account_in_container is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        container.update(updated_account.dict(), synchronize_session=False)
        db.commit()

        return container.first()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
#           DELETE ACCOUNT              
@router.delete('/delete_account')
def delete_user_account(db:Session = Depends(get_db), user_id=Depends(auth_handler.auth_wrapper)):
    """
    DESCRIPTION: this function deletes a user account from the database.
    @param db - the database session.
    @param user_id - the user id.
    @returns a response indicating the account was deleted.
    """
    try:
        account_container = db.query(alchemyModels.UserAcc).filter(alchemyModels.UserAcc.id == user_id)

        #NOTE: if account not found, raise 404 error
        if account_container.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        account_container.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    