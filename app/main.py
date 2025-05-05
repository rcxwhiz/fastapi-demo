from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import auth, db
from app.routers import users, widgets


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    db.create_db_and_tables()
    yield
    # cleanup


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(widgets.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
