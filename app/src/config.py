# -*- coding: utf-8 -*-

from os import environ as env

from pydantic import BaseModel, Field

class AppConfig(BaseModel):
    """
    Конфигурация приложения.

    Attributes:
        host (str): Хост приложения.
        port (int): Порт приложения.
    """
    host: str = Field(alias='APP_HOST')
    port: int = Field(alias='APP_PORT')


class ClickhouseConfig(BaseModel):
    """
    Конфигурация базы данных ClickHouse.

    Attributes:
        username (str): Имя пользователя для подключения к базе данных.
        password (str): Пароль для подключения к базе данных.
        host (str): Хост базы данных.
        port (str): Порт базы данных.
        database (str): Имя базы данных.
    """
    username: str = Field(alias='CLICKHOUSE_USERNAME')
    password: str = Field(alias='CLICKHOUSE_PASSWORD')
    host: str = Field(alias='CLICKHOUSE_HOST')
    port: str = Field(alias='CLICKHOUSE_PORT')
    database: str = Field(alias='CLICKHOUSE_DATABASE')


class RequestsConfig(BaseModel):
    """
    Конфигурация запросов.

    Attributes:
        api_url (str): URL для API запросов.
    """
    api_url: str = Field(default_factory=lambda: env['API_URL'])


class RetriesConfig(BaseModel):
    """
    Конфигурация повторных попыток запросов.

    Attributes:
        max_retries (int): Максимальное количество повторных попыток.
    """
    max_retries: int = Field(default_factory=lambda: int(env['MAX_RETRIES']))


class TableStyles(BaseModel):
    """
    Конфигурация стилей таблиц.

    Attributes:
        width (int): Максимальная ширина поля таблицы.
    """
    width: int = Field(default_factory=lambda: int(env['TABLE_FIELD_MAX']))


class Config(BaseModel):
    """
    Общая конфигурация приложения.

    Attributes:
        app (AppConfig): Конфигурация приложения.
        clickhouse (ClickhouseConfig): Конфигурация базы данных ClickHouse.
    """
    app: AppConfig = Field(default_factory=lambda: AppConfig(**env))
    clickhouse: ClickhouseConfig = Field(default_factory=lambda: ClickhouseConfig(**env))
