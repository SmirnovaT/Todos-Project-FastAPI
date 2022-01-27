from fastapi import FastAPI
import models
from database import engine

import routers.auth as api
import routers.todos as api

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(api.auth_router)
app.include_router(api.todos_router)
