from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (HTTP_200_OK,
                              HTTP_400_BAD_REQUEST,
                              HTTP_401_UNAUTHORIZED,
                              HTTP_500_INTERNAL_SERVER_ERROR,)

from .models import User
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


##########################
##########################

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
#     user = fake_decode_token(token=token)
#
#     if not user:app
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

    try:
        danny = User(first=f"daenerys",
                     last=f"targaryen",
                     username=f"khaleesi-of-the-great-grass-sea",
                     email=f"mother@dragons.ca")
        session.add(danny)
        await session.commit()
    except Exception as err:
        print(f"[db_error]\n::{err=}::\n")
        return HTMLResponse(content="ded",
                            status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    statement = select(User)
    result = await session.scalars(statement)

    if not result.one():
        return HTMLResponse(content="major error yikes",
                            status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    await session.execute(delete(User))
    await session.commit()

    return HTMLResponse(content="healthy",
                        status_code=HTTP_200_OK)



# routes/endpoints
@app.get(path="/")
async def index(request: Request) -> Response:
    return template.TemplateResponse(
        name="login.html",
        context={"request": request},
        media_type="text/html",
    )


# need to transform into using models
# @app.post(path="/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
#
#     username = fake_db.get(form_data.username)
#     if not username:
#         raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid username")
#
#     if not form_data.password == fake_db.get(form_data.password):
#         raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid password")
#
#     return {
#         "access_token": username,
#         "token_type": "bearer",
#     }


# @app.get(path="/users/me")
# async def read_users_me(curr_user: Annotated[User, Depends(get_current_user)]) -> User:
#     return curr_user




