from fastapi import FastAPI

from app import auth, db
from app.models import users

app = FastAPI()

db.register(app)
auth.register(app)

app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
