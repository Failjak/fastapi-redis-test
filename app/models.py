import re

from pydantic import BaseModel, validator, Field


class Address(BaseModel):
    address: str = Field(..., example="Paradise")


class Phone(BaseModel):
    phone: str = Field(..., example="8909777777")

    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(\+?)[1-9]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class UserInfo(Phone, Address):
    pass
