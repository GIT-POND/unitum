from fastapi import FastAPI
# from .database import engine
from App.routers import userAcc,taskList,task,userAuth
from .database import engine
from. import alchemyModels

# Cross Origin Resource Sharing
from fastapi.middleware.cors import CORSMiddleware

app  = FastAPI()

alchemyModels.Base.metadata.create_all(bind=engine) # needed to initialize database

origins = [
    #* specify domain of your web app here
    *
    # "https://www.my_website_domain.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #* allow specific http methods
    allow_headers=["*"],
)

'''
#* after adding alembic, the code below isn't needed to create all tables on startup
alchemyModels.Base.metadata.create_all(bind=engine) 
'''

#       APP ROUTES          
app.include_router(userAcc.router)
app.include_router(taskList.router)
app.include_router(task.router)
app.include_router(userAuth.router)

@app.get('/')
def root():
    return {'success':'Hello World'}