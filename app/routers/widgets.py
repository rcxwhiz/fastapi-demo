from fastapi import APIRouter, Form, HTTPException

from app.auth import CurrentActiveUserDep
from app.db import DBSessionDep
from app.models import User, Widget

router = APIRouter()


@router.post("/widgets", response_model=Widget)
def create_widget(
    db_session: DBSessionDep,
    user: CurrentActiveUserDep,
    title: str = Form(...),
    description: str | None = Form(None),
):
    db_session.add(Widget(title=title, description=description, owner=user.username))
    db_session.commit()
    return Widget(title=title, description=description, owner=user.username)


@router.delete("/widgets/{id}")
def delete_widget(db_session: DBSessionDep, user: CurrentActiveUserDep, id: int):
    widget = db_session.query(Widget).get(id)
    if widget is None:
        raise HTTPException(status_code=404, detail="Widget not found")
    if widget.owner != user.username:
        raise HTTPException(
            status_code=403, detail="You are not the owner of the widget"
        )
    db_session.delete(widget)
    db_session.commit()


@router.get("/widgets/{id}", response_model=Widget)
def get_widget(db_session: DBSessionDep, id: int):
    widget = db_session.query(Widget).get(id)
    if widget is None:
        raise HTTPException(status_code=404, detail="Widget not found")
    return widget


@router.get("/user/{username}/widgets", response_model=list[Widget])
def get_user_widgets(db_session: DBSessionDep, username: str):
    user = db_session.query(User).get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return list(user.widgets)
