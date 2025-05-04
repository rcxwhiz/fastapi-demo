from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    active: bool = Field(nullable=False)
