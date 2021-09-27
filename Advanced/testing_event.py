import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = {}


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


def test_read_items():
    with TestClient(app) as client:
        response = client.get("/items/foo")
        assert response.status_code == 200
        assert response.json() == {"name": "Fighters"}


test_read_items()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
