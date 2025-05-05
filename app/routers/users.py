from fastapi import APIRouter, Form, HTTPException
from passlib.context import CryptContext
from sqlmodel import select

from app.auth import CurrentActiveUserDep
from app.db import DBSessionDep
from app.models import PublicUser, User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/user", response_model=PublicUser)
def create_user(
    db_session: DBSessionDep, username: str = Form(...), password: str = Form(...)
):
    if db_session.exec(select(User).where(User.username == username)).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    db_session.add(User(username=username, hashed_password=pwd_context.hash(password)))
    db_session.commit()
    return PublicUser(username=username, active=True)


@router.get("/user/me", response_model=PublicUser)
def self_user(user: CurrentActiveUserDep):
    return user


@router.get("/user/{username}", response_model=PublicUser)
def get_user(username: str, db_session: DBSessionDep):
    user = db_session.query(User).filter_by(username=username).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_public()


@router.delete("/user/me")
def delete_user(user: CurrentActiveUserDep, db_session: DBSessionDep):
    db_session.delete(user)
    db_session.commit()
