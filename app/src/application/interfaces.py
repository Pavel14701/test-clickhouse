# -*- coding: utf-8 -*-

from typing import Protocol, Type
from abc import abstractmethod

from aiohttp import ClientSession
from pydantic import BaseModel

from app.src.config import RequestsConfig
from app.src.infrastructure.types import F


class Cruds(Protocol):
    """
    Протокол для операций CRUD.

    Methods:
        save_raw_data() -> str: Асинхронный метод для сохранения необработанных данных.
        get_raw_data() -> F: Асинхронный метод для получения необработанных данных.
        get_result_table() -> F: Асинхронный метод для получения результирующей таблицы.
    """

    @abstractmethod
    async def save_raw_data(self) -> str:
        ...

    @abstractmethod
    async def get_raw_data(self) -> F:
        ...

    @abstractmethod
    async def get_result_table(self) -> F:
        ...


class HttpParser(Protocol):
    """
    Протокол для парсинга данных по HTTP.

    Methods:
        get_data(url: str) -> str: Асинхронный метод для получения данных по указанному URL.
    """

    @abstractmethod
    async def get_data(self, url: str) -> str:
        ...


class TablesOptimizer(Protocol):
    """
    Протокол для оптимизации таблиц.

    Methods:
        optimize_raw_table() -> None: Асинхронный метод для оптимизации необработанных таблиц.
        optimize_parsed_table() -> None: Асинхронный метод для оптимизации распарсенных таблиц.
    """

    @abstractmethod
    async def optimize_raw_table(self) -> None:
        ...

    @abstractmethod
    async def optimize_parsed_table(self) -> None:
        ...


class ResponseTable(Protocol):
    """
    Протокол для создания таблиц ответов.

    Methods:
        create_response_table(schema: list[Type[BaseModel]]) -> str: Асинхронный метод для создания таблицы ответов.
    """

    @abstractmethod
    async def create_response_table(
        self,
        schema: list[Type[BaseModel]]
    ) -> str:
        ...


class ClientSessionGenerator(Protocol):
    """
    Протокол для генерации клиентских сессий.

    Methods:
        __call__() -> ClientSession: Асинхронный метод для создания клиентской сессии.
    """

    async def __call__(self) -> ClientSession:
        ...


class UrlGetter(Protocol):
    """
    Протокол для получения конфигурации URL.

    Methods:
        __call__() -> RequestsConfig: Асинхронный метод для получения конфигурации запросов.
    """

    async def __call__(self) -> RequestsConfig:
        ...
