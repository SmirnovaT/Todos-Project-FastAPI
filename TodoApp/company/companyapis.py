from fastapi import APIRouter

company_router = APIRouter()


@company_router.get("/")
async def get_company_name():
    return {"company_name": "Example Company, LLC"}


@company_router.get("/employees")
async def number_of__employees():
    return 162