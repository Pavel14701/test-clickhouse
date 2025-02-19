# -*- coding: utf-8 -*-

from typing import AsyncIterable, Iterable

from aiohttp import ClientSession
from dishka import Provider, Scope, provide, from_context
from sqlalchemy.orm import Session, sessionmaker

from app.src.application.interactors import (
    AddJsonInteractor, GetParsedDataInteractor
)
from app.src.application import interfaces
from app.src.config import (
    Config, 
    RequestsConfig, 
    RetriesConfig,
    TableStyles
)
from app.src.infrastructure.database import new_session_maker
from app.src.infrastructure.request import new_request_session_maker, SessionManager
from app.src.infrastructure.gateways import (
    CrudsGateway,
    HttpParserGateway, 
    ResponseTableGateway, 
    TablesOptimizerGateway
)

class MigrationsProvider(Provider):
    """
    Провайдер для миграций баз данных.

    Attributes:
        config (Config): Конфигурация приложения.
    """
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def sync_get_session_maker(
        self, 
        config: Config
    ) -> sessionmaker[Session]:
        """
        Создает sessionmaker для базы данных ClickHouse.

        Args:
            config (Config): Конфигурация приложения.

        Returns:
            sessionmaker[Session]: Фабрика сессий для базы данных ClickHouse.
        """
        return new_session_maker(config.clickhouse)

    @provide(scope=Scope.REQUEST)
    def sync_get_session(
        self, 
        session_maker: sessionmaker[Session]
    ) -> Iterable[Session]:
        """
        Предоставляет сессию базы данных для каждого запроса.

        Args:
            session_maker (sessionmaker[Session]): Фабрика сессий для базы данных ClickHouse.

        Yields:
            Iterable[Session]: Сессия базы данных.
        """
        with session_maker() as session:
            yield session


class AppProvider(Provider):
    """
    Основной провайдер приложения.

    Attributes:
        config (Config): Конфигурация приложения.
        request_config (RequestsConfig): Конфигурация запросов.
        retries_config (RetriesConfig): Конфигурация повторных попыток запросов.
        table_style_response_config (TableStyles): Конфигурация стилей таблиц.
    """
    config = from_context(provides=Config, scope=Scope.APP)
    request_config = from_context(provides=RequestsConfig, scope=Scope.APP)
    retries_config = from_context(provides=RetriesConfig, scope=Scope.APP)
    table_style_response_config = from_context(provides=TableStyles, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, 
        config: Config
    ) -> sessionmaker[Session]:
        """
        Создает sessionmaker для базы данных ClickHouse.

        Args:
            config (Config): Конфигурация приложения.

        Returns:
            sessionmaker[Session]: Фабрика сессий для базы данных ClickHouse.
        """
        return new_session_maker(config.clickhouse)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, 
        session_maker: sessionmaker[Session]
    ) -> AsyncIterable[Session]:
        """
        Асинхронно предоставляет сессию базы данных для каждого запроса.

        Args:
            session_maker (sessionmaker[Session]): Фабрика сессий для базы данных ClickHouse.

        Yields:
            AsyncIterable[Session]: Сессия базы данных.
        """
        with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_request_session(self) -> SessionManager[ClientSession]:
        """
        Создает новый менеджер сессий для aiohttp.

        Returns:
            SessionManager[ClientSession]: Новый менеджер сессий для aiohttp.
        """
        return new_request_session_maker()

    @provide(scope=Scope.REQUEST)
    async def get_client_session(
        self,
        session_maker: SessionManager[ClientSession]
    ) -> AsyncIterable[ClientSession]:
        """
        Асинхронно предоставляет клиентскую сессию для каждого запроса.

        Args:
            session_maker (SessionManager[ClientSession]): Менеджер сессий для aiohttp.

        Yields:
            AsyncIterable[ClientSession]: Клиентская сессия aiohttp.
        """
        session = await session_maker.create_session()
        try:
            yield session
        finally:
            await session.close()

    cruds_gateway = provide(
        CrudsGateway,
        scope=Scope.REQUEST,
        provides=interfaces.Cruds
    )

    table_optimizer = provide(
        TablesOptimizerGateway,
        scope=Scope.REQUEST,
        provides=interfaces.TablesOptimizer
    )

    table_response = provide(
        ResponseTableGateway,
        scope=Scope.REQUEST,
        provides=interfaces.ResponseTable
    )
    parser = provide(
        HttpParserGateway,
        scope=Scope.REQUEST,
        provides=interfaces.HttpParser
    )
    save_json_interactor = provide(
        AddJsonInteractor, scope=Scope.REQUEST
    )
    get_parsed_data_interactor = provide(
        GetParsedDataInteractor, scope=Scope.REQUEST
    )
