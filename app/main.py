from fastapi import FastAPI, HTTPException, BackgroundTasks
import aioredis
from base64 import urlsafe_b64encode
from hashlib import md5

from app.schemas import URLShort, URLBase, URLStore
from app.settings import app_settings, redis_settings

app = FastAPI(
    version=app_settings.app_version
)
redis = aioredis.from_url(redis_settings.redis_url, db=redis_settings.redis_db, decode_responses=True)


def get_key(url: str, salt: str = '') -> str:
    # add salt (in case of collisions) -> get md5 hash -> base64 encode -> truncate to 12 chars
    return urlsafe_b64encode(md5((salt + url).encode()).digest())[:12].decode()


@app.get("/")
def root():
    return {"message": "URL shortener app"}


@app.post("/urls", response_model=URLShort)
async def create_short_url(url: URLBase):
    salt = 0
    # loop to avoid collisions:
    while True:
        key = get_key(url.target_url, str(salt))
        url_db_data = await redis.hgetall(key)
        if not url_db_data:
            await redis.hmset(key, URLStore(target_url=url.target_url, count=0).dict())
            break
        elif url_db_data['target_url'] != url.target_url:
            salt += 1
        else:
            break
    return URLShort.from_key(key)


async def incr_count(key):
    await redis.hincrby(key, 'count', 1)


@app.get("/{key}", response_model=URLBase)
async def get_full_url(key: str, background_tasks: BackgroundTasks):

    url_db_data = await redis.hgetall(key)
    if not url_db_data:
        raise HTTPException(status_code=404, detail="URL not found")
    else:
        background_tasks.add_task(incr_count, key)
        return URLBase(target_url=url_db_data['target_url'])


@app.get("/urls/{key}", response_model=URLStore)
async def get_url_stats(key: str, background_tasks: BackgroundTasks):

    url_db_data = await redis.hgetall(key)
    if not url_db_data:
        raise HTTPException(status_code=404, detail="URL not found")
    else:
        return URLStore.parse_obj(url_db_data)
