import app.app_config
from fastapi import FastAPI
from app.auth.router import auth_routes
from app.test.router import test_routes

app = FastAPI()

app.include_router(auth_routes)
app.include_router(test_routes)


@app.get('/')
def Home():
    return 'welcome to fastapi'
