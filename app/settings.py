from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ServerSettings(Settings):
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"
    scheme: str = 'http'


class AppSettings(Settings):
    app_version: str = "local"
    app_domain: str = "tier.app"


class RedisSettings(Settings):
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"


server_settings = ServerSettings()
app_settings = AppSettings()
redis_settings = RedisSettings()
