from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Field
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from .database import initialize_database



APP_INFO: dict = {
    "title": "faster-next-app",
    "version": "0.0.0",
}


# application setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
template = Jinja2Templates(directory="frontend/")



# actual db settings
async def on_startup():
    await initialize_database()

def get_application() -> FastAPI:
    fastapi_app = FastAPI(**APP_INFO)

    fastapi_app.add_event_handler(
        event_type="startup",
        func=on_startup,
    )

    return fastapi_app


# Wrapper class to package event handler nicely, init og db
app: FastAPI = get_application()


# fake data
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

##########################
##########################

# models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    first_name: str
    last_name: str
    username: str
    email: str = Field(default=None, unique=True)
    is_active: bool


class UserInDB(User):
    hashed_pw: str


# helpers
def fake_pw_hash(password: str) -> str:
    return f"fakehash{password}"


def get_user(db, username: str) -> User:
    if username in db:
        user_dict: dict = db[username]

        return UserInDB(**user_dict)


def fake_decode_token(token) -> User:
    user = get_user(
        db=fake_db,
        username=token,
    )

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = fake_decode_token(token=token)

    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# routes/endpoints
@app.get(path="/")
async def index(request: Request) -> Response:
    return template.TemplateResponse(
        name="login.html",
        context={"request": request},
        media_type="text/html",
    )



@app.post(path="/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:

    user_dict = fake_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Invalid username/password")

    user = UserInDB(**user_dict)

    hashed_password = fake_pw_hash(password=form_data.password)
    if not hashed_password:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Invalid username/password")

    return {
        "access_token": user.username,
        "token_type": "bearer",
    }


@app.get(path="/users/me")
async def read_users_me(curr_user: Annotated[User, Depends(get_current_user)]) -> User:
    return curr_user


























