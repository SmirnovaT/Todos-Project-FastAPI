from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.auth_router)
app.include_router(todos.todos_router)