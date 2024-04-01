from typing import Optional

from pydantic import EmailStr
from sqlmodel import AutoString, Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    first: str
    last: str
    username: str
    email: EmailStr = Field(unique=True, sa_type=AutoString)
    is_active: bool = True

    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"


# fake data; not being used
fake_db: dict = {
    "danny": {
        "first": "daenerys",
        "last": "targaryen",
        "username": "khaleesi",
        "hashed_pw": "fakehashdannypw",
        "email": "mother@dragons.ca",
        "is_active": True,
    },
    "arthur": {
        "first": "arthur",
        "last": "dayne",
        "username": "arthur",
        "hashed_pw": "fakehasharthurpw",
        "email": "dual@wielder.com",
        "is_active": False,
    },
    "barry": {
        "first": "barriston",
        "last": "selmy",
        "username": "barry",
        "hashed_pw": "fakehashbarrypw",
        "email": "greatest@swordsman.uk",
        "is_active": True,
    },
}

