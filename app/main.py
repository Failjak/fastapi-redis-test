import json

from fastapi import FastAPI, Depends, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from redis import asyncio as aioredis
from starlette.responses import JSONResponse

from app.config import redis_config
from app.models import UserInfo, Phone, Address

app = FastAPI()
redis = aioredis.from_url(redis_config.url, encoding="utf8", decode_responses=True)


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    exc_json = json.loads(exc.json())
    return JSONResponse({"error": exc_json}, status_code=422)


@app.get("/")
async def root():
    return {"message": "Hello worlddddd"}


@app.post("/write_data", response_model=UserInfo)
async def save_user_data(user_data: UserInfo):
    await redis.set(user_data.phone, user_data.address)
    return user_data


@app.put(
    "/write_data",
    response_model=Address,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Phone, "description": "The address was not found"},
        status.HTTP_200_OK: {
            "description": "Address has been changed",
            "content": {
                "application/json": {
                    "example": {"address": "New Paradise"}
                }
            },
        },
    }
)
async def update_user_data(user_data: UserInfo):
    if not await redis.get(user_data.phone):
        return JSONResponse(status_code=404,
                            content={'message': f'Address for this phone did not saved: {user_data.phone}'})
    await redis.set(user_data.phone, user_data.address)
    return Address(address=user_data.address)


@app.get(
    "/check_data/{phone}",
    response_model=Address,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Phone, "description": "The address was not found"},
        status.HTTP_200_OK: {
            "description": "Address requested by Phone",
            "content": {
                "application/json": {
                    "example": {"address": "Paradise"}
                }
            },
        },

    })
async def get_user_data(phone: Phone = Depends()):
    if user_address := await redis.get(phone.phone):
        return Address(address=user_address)
    return JSONResponse(status_code=404,
                        content={'message': f"The address for this phone: {phone.phone} hasn't been saved"})
