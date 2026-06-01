from pathlib import Path
import os
from decouple import Config, RepositoryEnv

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILES = [ROOT_DIR / '.env', ROOT_DIR / '.env.compose']

def get_config() -> Config:
    for env_file in ENV_FILES:
        if env_file.exists():
            return Config(RepositoryEnv(str(env_file)))
    # Fall back to environment variables only
    return Config(repository=os.environ)

config = get_config()

DATABASE_URL = config('DATABASE_URL', default='')
DB_TIMEZONE = config('DB_TIMEZONE', default='UTC')
