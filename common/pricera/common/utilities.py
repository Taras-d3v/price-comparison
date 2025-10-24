import os
from typing import Optional


def get_env_value(env_name: str) -> Optional[str]:
    return os.getenv(env_name)


def get_rabbitmq_host() -> Optional[str]:
    return get_env_value("RABBIT_MQ_HOST")


def get_rabbitmq_user() -> Optional[str]:
    return get_env_value("RABBIT_MQ_USER")


def get_rabbitmq_password() -> Optional[str]:
    return get_env_value("RABBIT_MQ_PASSWORD")
