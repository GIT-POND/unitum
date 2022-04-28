from pydantic import BaseSettings


class Settings(BaseSettings):
    '''
        This class ensures essential environment variables
        are set. These variables are user to connect to
        the database or generate a jwt token.
    '''
    database_username: str
    database_password: str
    database_host: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"  # get values from .env file in same directory
        env_file_encoding = "utf-8"


settings = Settings()