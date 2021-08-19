import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, HTMLResponse, PlainTextResponse, \
    RedirectResponse, StreamingResponse, FileResponse

app = FastAPI()


@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]


@app.get("/items2/", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"


@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


@app.get("/streaming")
async def streaming():
    return StreamingResponse(fake_video_streamer())


some_file_path = "large-video-file.mp4"


@app.get("/streaming2")
def streaming2():
    def iterfile():  # (1)
        with open(some_file_path, mode="rb") as file_like:  # (2)
            yield from file_like  # (3)
    return StreamingResponse(iterfile(), media_type="video/mp4")


@app.get("/file")
async def main():
    return FileResponse(some_file_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
