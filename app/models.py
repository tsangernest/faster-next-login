from functools import cached_property
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

    @cached_property
    def fullname(self) -> str:
        return f"{self.first} {self.last}"


# fake data; not being used
fake_db: dict = {
    "danny": {
        "first_name": "daenerys",
        "last_name": "targaryen",
        "username": "danny",
        "hashed_pw": "fakehashdannypw",
        "email": "mother@dragons.ca",
        "is_active": True,
    },
    "arthur": {
        "first_name": "arthur",
        "last_name": "dayne",
        "username": "arthur",
        "hashed_pw": "fakehasharthurpw",
        "email": "dual@wielder.com",
        "is_active": False,
    },
    "barry": {
        "first_name": "barriston",
        "last_name": "selmy",
        "username": "barry",
        "hashed_pw": "fakehashbarrypw",
        "email": "greatest@swordsman.uk",
        "is_active": True,
    },
}

