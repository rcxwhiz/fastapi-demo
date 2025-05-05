from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    active: bool = Field(default=True, nullable=False)

    def to_public(self):
        return PublicUser(username=self.username, active=self.active)


class PublicUser(SQLModel):
    username: str
    active: bool
