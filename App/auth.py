import jwt # Token encoding/decoding
from fastapi import HTTPException, Security # dependency injection
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from  datetime import datetime, timedelta
from .config import settings as set



class AuthHandler():
    
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hash_password(self, password):
        return self.pwd_context.hash(password)
    

    def verify_password(self, plain_pw, hashed_pw):
        return self.pwd_context.verify(plain_pw, hashed_pw)


    def encode_token(self, user_id):
        """
        DESCRIPTION: Encode a JWT token for the user.   
        @param user_id - the user id for the token.     
        @returns the encoded token.                  """

        payload = {
            'exp':datetime.utcnow() + timedelta(hours=1), # set expiration time
            'iat':datetime.utcnow(), # set time issued
            'sub':user_id # set subject id
        }
        return jwt.encode(
            payload,
            set.secret_key,
            algorithm=set.algorithm
        )


    def decode_token(self, token):
        """
        DESCRIPTION: Decode the token and return the user id.   
        @param token - the token to decode                      
        @return the user id                                  """
        try:
            payload = jwt.decode(token, set.secret_key, algorithms=['HS256'])
            return payload['sub'] # return user_id

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='signature expired')
        except jwt.InvalidTokenError as err:
            raise HTTPException(status_code=401, detail='invalid token')
    

    def auth_wrapper(self, auth:HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
