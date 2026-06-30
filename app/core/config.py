from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_use_a_long_random_string"

    class Config:
        env_file = ".env"


settings = Settings()


# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     DATABASE_URL: str

#     class Config:
#         env_file = ".env"


# settings = Settings()
