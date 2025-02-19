# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.src.config import ClickhouseConfig


def new_session_maker(config: ClickhouseConfig) -> sessionmaker[Session]:
    """
    Создает новый sessionmaker для подключения к базе данных ClickHouse.

    Args:
        config (ClickhouseConfig): Конфигурация для подключения к базе данных ClickHouse.

    Returns:
        sessionmaker[Session]: Фабрика сессий для взаимодействия с базой данных ClickHouse.
    """
    database_uri = "clickhouse+native://{username}:{password}@{host}:{port}/{database}".format(
        username=config.username,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database,
    )

    engine = create_engine(
        database_uri,
        pool_size=5,
        max_overflow=5,
    )
    return sessionmaker(engine, class_=Session)
