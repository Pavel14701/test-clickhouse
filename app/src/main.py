#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiohttp.web_routedef import RouteTableDef
from dishka import make_async_container
from dishka.integrations.aiohttp import (
    DISHKA_CONTAINER_KEY,
    AiohttpProvider,
    setup_dishka,
)

from app.src.config import (
    Config, RequestsConfig, RetriesConfig, TableStyles
)
from app.src.ioc import AppProvider
from app.src.controllers.http import router

logging.basicConfig(level=logging.DEBUG)

def get_aiohttp_app(router: RouteTableDef) -> Application:
    """
    Создает и настраивает приложение aiohttp с маршрутами.

    Args:
        router (RouteTableDef): Маршруты для приложения.

    Returns:
        Application: Настроенное приложение aiohttp.
    """
    aiohttp_app = Application()
    aiohttp_app.add_routes(router)
    return aiohttp_app

async def on_shutdown(app: Application) -> None:
    """
    Асинхронный обработчик для закрытия контейнера Dishka при завершении работы приложения.

    Args:
        app (Application): Приложение aiohttp.
    """
    await app[DISHKA_CONTAINER_KEY].close()

def main() -> None:
    """
    Основная функция для инициализации и запуска приложения aiohttp.
    """
    config = Config()
    request_config = RequestsConfig()
    retries_config = RetriesConfig()
    tables_config = TableStyles()
    app = get_aiohttp_app(router)
    container = make_async_container(
        AppProvider(), 
        AiohttpProvider(), 
        context={
            Config: config,
            RequestsConfig: request_config,
            RetriesConfig: retries_config,
            TableStyles: tables_config
        }
    )
    setup_dishka(container=container, app=app)
    app.on_shutdown.append(on_shutdown)
    run_app(app)

if __name__ == "__main__":
    main()
