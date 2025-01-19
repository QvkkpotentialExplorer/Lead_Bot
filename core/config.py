from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)
print(BASE_DIR)
class Setting(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/bot.db"
    db_echo: bool = True


settings = Setting()
