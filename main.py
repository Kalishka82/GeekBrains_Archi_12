from fastapi import FastAPI
import uvicorn
from starlette import status
from starlette.responses import RedirectResponse
from contextlib import asynccontextmanager

from db.db import database
from routers import client, pet, consultation


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(client.router, tags=["client"])
app.include_router(pet.router, tags=["pet"])
app.include_router(consultation.router, tags=["concultation"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
