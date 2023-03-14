import os
from app.auth import OA2Token, parse_token
from fastapi import APIRouter, Depends

test_routes = APIRouter()


@test_routes.get('/test')
def test(token: OA2Token = Depends()):
    return parse_token(token)
