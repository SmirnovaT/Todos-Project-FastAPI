from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos
from company import companyapis, dependencies


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.auth_router)
app.include_router(todos.todos_router)
app.include_router(
    companyapis.company_router,
    prefix="/companyapis",
    tags=["companysapis"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "Internal Use Only"}}
    )

