import os
from typing import Optional


def get_env_value(env_name: str) -> Optional[str]:
    return os.getenv(env_name)
