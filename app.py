from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from src.routers.v1 import router_v1
from src.config.config import get_settings
from src.config.firebase_admin import initialize_firebase_admin


SETTINGS = get_settings()

def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize_firebase_admin()
    yield

app = FastAPI(
    title=SETTINGS.API_NAME, 
    openapi_url=f"{SETTINGS.API_V1_STR}/openapi.json",
    version=SETTINGS.REVISION,
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_v1.api_router, prefix=SETTINGS.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True, port=3000, host='0.0.0.0')