from pydantic import BaseSettings


class RedisConfig(BaseSettings):
    url: str

    class Config:
        env_prefix = 'REDIS_'
        env_file = '.env'


redis_config = RedisConfig()
