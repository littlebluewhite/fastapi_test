from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

app = FastAPI()


@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        },
    },
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "there goes my hero"}
    else:
        return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get(
    "/items2/{item_id}",
    response_model=Item,
    responses={**responses, 200: {"content": {"image/png": {}}}}
)
async def read_item(item_id: str, img: Optional[bool] = None):
    if img:
        return FileResponse("image.png", media_type="image/png")
    else:
        return Item(id=item_id, value="happy")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
