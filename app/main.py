from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import SQLModel, Field
from starlette.status import (HTTP_200_OK,
                              HTTP_400_BAD_REQUEST,
                              HTTP_401_UNAUTHORIZED,
                              HTTP_500_INTERNAL_SERVER_ERROR,)

from .database import get_async_session, initialize_database



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


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
#     user = fake_decode_token(token=token)
#
#     if not user:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED,
#             detail="Invalid login credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     return user


@app.get(path="/health",
         response_class=HTMLResponse,
         responses={HTTP_200_OK: {"db_conn": "healthy"},
                    HTTP_500_INTERNAL_SERVER_ERROR: {"db_conn": "ded"}})
async def health_check(
    session: Annotated[AsyncSession, Depends(dependency=get_async_session)],
) -> HTMLResponse:
    return HTMLResponse



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

    username = fake_db.get(form_data.username)
    if not username:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid username")

    if not form_data.password == fake_db.get(form_data.password):
        raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid password")

    return {
        "access_token": username,
        "token_type": "bearer",
    }


# @app.get(path="/users/me")
# async def read_users_me(curr_user: Annotated[User, Depends(get_current_user)]) -> User:
#     return curr_user




