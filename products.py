from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

PRODUCTS = {
    'product_1': {'title': 'Title One', 'price': 'Price One'},
    'product_2': {'title': 'Title Two', 'price': 'Price Two'},
    'product_3': {'title': 'Title Three', 'price': 'Price Three'},
    'product_4': {'title': 'Title Four', 'price': 'Price Four'},
    'product_5': {'title': 'Title Five', 'price': 'Price Five'}
}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"


@app.get("/")
async def read_all_products(skip_product: Optional[str] = None):
    if skip_product:
        new_products = PRODUCTS.copy()
        del new_products[skip_product]
        return new_products
    return PRODUCTS


@app.get("/{product_title}")
async def read_product(product_title: str):
    return PRODUCTS[product_title]

@app.post("/")
async def create_product(product_title, product_price: int):
    current_product_id = 0

    if len(PRODUCTS) > 0:
        for product in PRODUCTS:
            x = int(product.split('_')[-1])
            if x > current_product_id:
                current_product_id = x
    PRODUCTS[f'product_{current_product_id +1}'] = {'title': product_title, 'price': product_price}
    return PRODUCTS[f'product_{current_product_id + 1}']


@app.put("/{product_title}")
async def update_product(product_title: str, product_price: int):
    product_information = {'title': product_title, 'price': product_price}
    PRODUCTS[product_title] = product_information
    return product_information


@app.delete("/{product_title}")
async def delete_product(product_title):
    del PRODUCTS[product_title]
    return f'Product {product_title} deleted.'



@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    return {"Direction": direction_name, "sub": "Left"}


@app.get("/products/{product_id}")
async def read_product(product_id):
    return {"product_title": product_id}

