import app.app_config
from fastapi import FastAPI
from app.auth.router import auth_routes
from app.test.router import test_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth_routes)
app.include_router(test_routes)


@app.get('/')
def Home():
    return 'welcome to fastapi'
