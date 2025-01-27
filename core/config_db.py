from pathlib import Path

from pydantic_settings import BaseSettings
from config import load_config
BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)
print(BASE_DIR)
db_path = load_config('.env').db.path
print(db_path)
class Setting(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{db_path}"
    db_echo: bool = True


settings = Setting()
