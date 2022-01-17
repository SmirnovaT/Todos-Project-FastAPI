from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, products_to_return):
        self.products_to_return = None
        self.products_to_return == products_to_return


app = FastAPI()


class Product(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    price: int = Field(gt=1)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)
    number: int = Field(gt=0, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "7b13b480-6b9b-43cb-bd4a-37cd3636f01c",
                "title": "Bread",
                "price": 32,
                "description": "very tasty",
                "number": 76
            }
        }


class ProductNoNumber(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    price: int = Field(gt=1)
    description: Optional[str] = Field(None, title="Description of the book",
                                       max_length=100,
                                       min_length=1)

PRODUCTS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.products_to_return}"
                            f"products? You need to read more!"}
    )


@app.post("/products/login")
async def product_login(username:str = Form(...), password: str = Form(...)):
    return {'username': username, 'password': password}


@app.get('/header')
async def read_header(random_header: Optional[str] = Header(None)):
    return {'Random-Header': random_header}


@app.get("/")
async def read_all_products(products_to_return: Optional[int] = None):
    if products_to_return and products_to_return < 0:
        raise NegativeNumberException(products_to_return=products_to_return)

    if len(PRODUCTS) < 1:
        create_products_no_api()

    if products_to_return and len(PRODUCTS) >= products_to_return > 0:
        i = 1
        new_products = []
        while i <= products_to_return:
            new_products.append(PRODUCTS[i - 1])
            i += 1
        return new_products
    return PRODUCTS


@app.get("/product/{product_id}")
async def read_product(product_id: UUID):
    for x in PRODUCTS:
        if x.id == product_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/product/number/{product_id}", response_model=ProductNoNumber)
async def read_product_no_number(product_id: UUID):
    for x in PRODUCTS:
        if x.id == product_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    PRODUCTS.append(product)
    return product


@app.put("/{product_id}")
async def update_product(product_id: UUID, product: Product):
    counter = 0

    for x in PRODUCTS:
        counter += 1
        if x.id == product_id:
            PRODUCTS[counter - 1] = product
            return PRODUCTS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{product_id}")
async def delete_product(product_id: UUID):
    counter = 0

    for x in PRODUCTS:
        counter += 1
        if x.id == product_id:
            del PRODUCTS[counter - 1]
            return f'ID:{product_id} deleted'
    raise raise_item_cannot_be_found_exception()


def create_products_no_api():
    product_1 = Product(id="e3b389a4-14df-40e5-954f-5ae9fdb5b6b6",
                        title="Title 1",
                        price=3,
                        description="Description 1",
                        number=1)
    product_2 = Product(id="2e3b389a4-14df-40e5-954f-5ae9fdb5b6b6",
                        title="Title 2",
                        price=4,
                        description="Description 2",
                        number=2)
    product_3 = Product(id="3e3b389a4-14df-40e5-954f-5ae9fdb5b6b6",
                        title="Title 3",
                        price=55,
                        description="Description 3",
                        number=3)
    product_4 = Product(id="4e3b389a4-14df-40e5-954f-5ae9fdb5b6b6",
                        title="Title 4",
                        price=53,
                        description="Description 4",
                        number=4)
    PRODUCTS.append(product_1)
    PRODUCTS.append(product_2)
    PRODUCTS.append(product_3)
    PRODUCTS.append(product_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail='Product not found',
                         headers={'X-Header_Error':
                                      'Nothing to be seen at the UUID'})
