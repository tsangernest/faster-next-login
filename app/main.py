from fastapi import FastAPI

from .api import router
from .database import initialize_database


APP_INFO: dict = {
    "title": "faster-next-app",
    "version": "0.0.0",
}


# Application setup
async def on_startup():
    await initialize_database()


def get_application() -> FastAPI:
    fastapi_app = FastAPI(**APP_INFO)

    fastapi_app.add_event_handler(event_type="startup", func=on_startup)
    fastapi_app.include_router(router=router)

    return fastapi_app

# Wrap everything nicely for app start
app: FastAPI = get_application()

