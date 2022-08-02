from pydantic.main import BaseModel


class URLBase(BaseModel):
    target_url: str


class URLShort(BaseModel):
    short_url: str