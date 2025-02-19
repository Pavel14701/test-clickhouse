# -*- coding: utf-8 -*-

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import functools
from typing import Any, Callable, Optional, Type

from aiohttp import ClientSession
from tabulate import tabulate
import textwrap
from sqlalchemy.orm import Session
import sqlalchemy as sa
from pydantic import BaseModel

from app.src.application.interfaces import (
    Cruds,
    HttpParser, 
    ResponseTable, 
    TablesOptimizer
)
from app.src.config import TableStyles
from app.src.controllers.schemas import (
    AstronautSchema,
    RawJsonSchema
)
from app.src.infrastructure.types import Z


class CrudsGateway(Cruds):
    """
    Класс для взаимодействия с базой данных через операции CRUD.

    Args:
        session (Session): Сессия SQLAlchemy для выполнения запросов.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def __unwrapped_save_raw_json(self, json_data: str) -> None:
        """
        Вставляет необработанные JSON данные в таблицу raw_table.

        Args:
            json_data (str): Необработанные данные JSON.
        """
        query = sa.text("""
            INSERT INTO raw_table (json_data)
            VALUES (:json_data)
        """)
        self._session.execute(
            statement=query,
            params={"json_data": json_data}
        )

    async def save_raw_data(self, data: str) -> None:
        """
        Асинхронно сохраняет необработанные данные JSON.

        Args:
            data (str): Необработанные данные JSON.
        """
        await run_in_thread(self.__unwrapped_save_raw_json, data)

    def __unwrapped_get_raw_data(self) -> list[RawJsonSchema]:
        """
        Извлекает необработанные данные из таблицы raw_table.

        Returns:
            list[RawJsonSchema]: Список необработанных данных в формате RawJsonSchema.
        """
        query = sa.text("""
            SELECT * FROM raw_table
        """)
        result = self._session.execute(query)
        return [RawJsonSchema(**row) for row in result.mappings()]

    async def get_raw_data(self) -> list[RawJsonSchema]:
        """
        Асинхронно получает необработанные данные из таблицы raw_table.

        Returns:
            list[RawJsonSchema]: Список необработанных данных в формате RawJsonSchema.
        """
        return await run_in_thread(self.__unwrapped_get_raw_data)

    def __unwrapped_get_result_table(self) -> list[AstronautSchema]:
        """
        Извлекает обработанные данные из таблицы parsed_table.

        Returns:
            list[AstronautSchema]: Список обработанных данных в формате AstronautSchema.
        """
        query = sa.text("""
            SELECT * FROM parsed_table
        """)
        result = self._session.execute(query)
        return [AstronautSchema(**row) for row in result.mappings()]

    async def get_result_table(self) -> list[AstronautSchema]:
        """
        Асинхронно получает обработанные данные из таблицы parsed_table.

        Returns:
            list[AstronautSchema]: Список обработанных данных в формате AstronautSchema.
        """
        return await run_in_thread(func=self.__unwrapped_get_result_table)


class TablesOptimizerGateway(TablesOptimizer):
    """
    Класс для оптимизации таблиц в базе данных ClickHouse.

    Args:
        session (Session): Сессия SQLAlchemy для выполнения запросов.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def __unwrapped_optimize_parsed_table(self) -> None:
        """
        Оптимизирует таблицу parsed_table.
        """
        query = sa.text("""
            OPTIMIZE TABLE parsed_table FINAL;
        """)
        self._session.execute(query)

    async def optimize_raw_table(self) -> None:
        """
        Асинхронно оптимизирует таблицу raw_table.
        """
        await run_in_thread(func=self.__unwrapped_optimize_raw_table)

    def __unwrapped_optimize_raw_table(self) -> None:
        """
        Оптимизирует таблицу raw_table.
        """
        query = sa.text("""
            OPTIMIZE TABLE raw_table FINAL;
        """)
        self._session.execute(query)

    async def optimize_parsed_table(self) -> None:
        """
        Асинхронно оптимизирует таблицу parsed_table.
        """
        await run_in_thread(func=self.__unwrapped_optimize_parsed_table)


class ResponseTableGateway(ResponseTable):
    """
    Класс для создания таблиц ответов.

    Args:
        config (TableStyles): Конфигурация стилей таблиц.
    """

    def __init__(self, config: TableStyles) -> None:
        self.config = config

    async def create_response_table(
        self, 
        schema: list[BaseModel]
    ) -> str:
        """
        Создает таблицу ответов на основе предоставленной схемы.

        Args:
            schema (list[BaseModel]): Список данных в формате BaseModel.

        Returns:
            str: Таблица ответов в виде строки.
        """
        field_names = {field: field.upper() for field in schema[0].model_fields.keys()}
        table_data = [
            {field_names[field]: await self.format_field(field, getattr(dto, field)) for field in field_names}
            for dto in schema
        ]
        for row in table_data:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        result = tabulate(
            tabular_data=table_data,
            headers="keys",
            tablefmt="grid"
        )
        return result

    async def format_field(self, field: str, value: str) -> str:
        """
        Форматирует значение поля.

        Args:
            field (str): Название поля.
            value (str): Значение поля.

        Returns:
            str: Форматированное значение поля.
        """
        if isinstance(value, str):
            return "\n".join(textwrap.wrap(value, width=self.config.width))
        return value


class HttpParserGateway(HttpParser):
    """
    Класс для парсинга данных по HTTP.

    Args:
        request_session (ClientSession): Сессия aiohttp для выполнения запросов.
    """

    def __init__(self, request_session: ClientSession) -> None:
        self._request_session = request_session

    async def get_data(self, url: str) -> str:
        """
        Получает данные по указанному URL.

        Args:
            url (str): URL для получения данных.

        Returns:
            str: Полученные данные в виде строки.

        Raises:
            aiohttp.ClientResponseError: Ошибка клиента при получении данных.
        """
        async with self._request_session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                await response.raise_for_status()


async def run_in_thread(
    func: Callable[..., Z],
    *args: Any
) -> Optional[Type[BaseModel]]:
    """
    Запускает функцию в отдельном потоке.

    Args:
        func (Callable[..., Z]): Функция для выполнения.
        *args (Any): Аргументы для функции.

    Returns:
        Optional[Type[BaseModel]]: Результат выполнения функции.
    """
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(
            executor=pool,
            func=functools.partial(func, *args)
        )