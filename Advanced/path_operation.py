from typing import Optional, Set

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic import BaseModel

app = FastAPI()


@app.get("/items/", operation_id="some_specific_id_you_define", include_in_schema=False)
async def read_items():
    return [{"item_id": "Foo"}]


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return item

use_route_names_as_operation_ids(app)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
