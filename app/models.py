from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    active: bool = Field(default=True, nullable=False)

    widgets: list["Widget"] = Relationship(back_populates="owner")

    def to_public(self):
        return PublicUser(username=self.username, active=self.active)


class PublicUser(SQLModel):
    username: str
    active: bool


class Widget(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    description: str = Field(nullable=True)

    owner_username: str = Field(foreign_key="user.username")
    owner: User = Relationship(back_populates="widgets")
