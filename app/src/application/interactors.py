# -*- coding: utf-8 -*-

from app.src.application.interfaces import (
    Cruds,
    HttpParser,
    ResponseTable,
    TablesOptimizer
)
from app.src.config import RequestsConfig


class AddJsonInteractor:
    """
    Класс, отвечающий за взаимодействие с JSON данными.

    Args:
        parser_gateway (HttpParser): Интерфейс для парсинга JSON данных.
        crud_gateway (Cruds): Интерфейс для операций CRUD.
        optimize_gateway (TablesOptimizer): Интерфейс для оптимизации таблиц.
        url_gateway (RequestsConfig): Конфигурация URL для получения данных.
        table_gateway (ResponseTable): Интерфейс для создания таблиц ответов.
    """

    def __init__(
        self,
        parser_gateway: HttpParser,
        crud_gateway: Cruds,
        optimize_gateway: TablesOptimizer,
        url_gateway: RequestsConfig,
        table_gateway: ResponseTable
    ) -> None:
        self._parser_gateway = parser_gateway
        self._crud_gateway = crud_gateway
        self._optimize_gateway = optimize_gateway
        self._url_gateway = url_gateway
        self._table_gateway = table_gateway

    async def __call__(self) -> str:
        """
        Основной метод для получения, сохранения и оптимизации данных,
        а также создания таблицы ответов.

        Returns:
            str: Результирующая таблица в формате строки.
        """
        data = await self._parser_gateway.get_data(self._url_gateway.api_url)
        await self._crud_gateway.save_raw_data(data)
        await self._optimize_gateway.optimize_raw_table()
        data = await self._crud_gateway.get_raw_data()
        return await self._table_gateway.create_response_table(data)


class GetParsedDataInteractor:
    """
    Класс, отвечающий за получение и оптимизацию распарсенных данных.

    Args:
        crud_gateway (Cruds): Интерфейс для операций CRUD.
        optimize_gateway (TablesOptimizer): Интерфейс для оптимизации таблиц.
        table_gateway (ResponseTable): Интерфейс для создания таблиц ответов.
    """

    def __init__(
        self,
        crud_gateway: Cruds,
        optimize_gateway: TablesOptimizer,
        table_gateway: ResponseTable
    ) -> None:
        self._crud_gateway = crud_gateway
        self._optimize_gateway = optimize_gateway
        self._table_gateway = table_gateway

    async def __call__(self) -> str:
        """
        Основной метод для оптимизации распарсенных данных и создания
        таблицы ответов.

        Returns:
            str: Результирующая таблица в формате строки.
        """
        await self._optimize_gateway.optimize_parsed_table()
        result = await self._crud_gateway.get_result_table()
        return await self._table_gateway.create_response_table(result)
