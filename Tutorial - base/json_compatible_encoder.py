from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    print(type(item))
    json_compatible_item_data = jsonable_encoder(item)
    print(type(json_compatible_item_data))
    print(json_compatible_item_data)
    fake_db[id] = json_compatible_item_data
