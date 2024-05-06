from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
)

from .auth import OIDCSettings, oidc_scheme
from .database import get_async_session
from .models import User


router = APIRouter()

template = Jinja2Templates(directory="frontend/")


@router.get(path="/health",
            response_class=HTMLResponse,
            responses={HTTP_200_OK: {"db_conn": "healthy"},
                       HTTP_500_INTERNAL_SERVER_ERROR: {"db_conn": "ded"}})
async def health_check(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> HTMLResponse:
    try:
        dany = User(first="daenerys",
                    last="targaryen",
                    username="khaleesi",
                    email="mother@dragons.ca")
        session.add(dany)
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


@router.get(path="/")
async def index(request: Request) -> Response:
    return template.TemplateResponse(
        name="login.html",
        context={"request": request},
        media_type="text/html",
    )


