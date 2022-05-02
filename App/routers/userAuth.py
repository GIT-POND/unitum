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
router = APIRouter(prefix='/auth', tags=['auth'])


#           VERIFY USERNAME
@router.post('/username_available', status_code=status.HTTP_200_OK)
def check_username_availability(user: pydanticModels.CheckUsername, db: Session = Depends(get_db)):
    """
    description: Check if the username is available.                
    @param user - the username to check for availability.           
    @param db - the database session.                               
    @returns true if the username is available, false otherwise.    
    """
    try:
        search_result = db.query(alchemyModels.UserAcc).filter(
            alchemyModels.UserAcc.username == user.username).first()

        # NOTE: If available, return true. Otherwise, return false.
        if search_result is None:
            return {'available': True}
        else:
            return {'available': False}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           ACCOUNT REGISTER
@router.post('/create_account', status_code=status.HTTP_201_CREATED, response_model=pydanticModels.UserAccResponse)
def create_account(user: pydanticModels.CreateUserAcc, db: Session = Depends(get_db)):
    """
    description:   Create the user account in the database and return it.   
    @param user - the user account to create.                               
    @param db - the database session.                                       
    @returns the new user account.                                          
    """
    try:
        hashed_pw = auth_handler.hash_password(user.password)
        user.password = hashed_pw

        new_user_account = alchemyModels.UserAcc(**user.dict())

        db.add(new_user_account)    # update db
        db.commit()     # save changes
        db.refresh(new_user_account)  # reload db data

        return new_user_account
    except BaseException as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


#           ACCOUNT LOGIN
@router.post('/login_account', status_code=status.HTTP_201_CREATED)
def login_account(user: pydanticModels.LoginUserAcc, db: Session = Depends(get_db)):
    """
    description:   Create the user account in the database and return it.   
    @param user - the user account to create.                               
    @param db - the database session.                                       
    @returns the new user account.                                          
    """
    try:
        db_user = db.query(alchemyModels.UserAcc).filter(
            alchemyModels.UserAcc.email == user.email).first()

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='invalid user')

        if auth_handler.verify_password(user.password, db_user.password):
            token = auth_handler.encode_token(db_user.id)
            return {'token': token}
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='invalid user')
    except BaseException as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
