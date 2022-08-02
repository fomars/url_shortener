import validators
from pydantic import validator
from pydantic.main import BaseModel
from app.settings import app_settings


class URLBase(BaseModel):
    target_url: str

    @validator("target_url")
    def assert_url_valid(cls, v):
        if not validators.url(v):
            raise ValueError("Please send a valid URL")
        return v


class URLShort(BaseModel):
    url: str

    @classmethod
    def from_key(cls, key: str):
        return cls(url=f"https://{app_settings.app_domain}/{key}")


class URLStore(URLBase):
    count: int = 0
