from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter

from app.api.main import api_router, user_router
from app.core.config import settings
from app.deps import get_user_from_key
from app.middleware import api_request_middleware


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(openapi_url="", debug=True)

app.middleware("http")(api_request_middleware)

user_app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

user_app.include_router(api_router)
user_app.include_router(user_router, dependencies=[Depends(get_user_from_key)])

app.mount(
    settings.API_V1_STR,
    user_app
)