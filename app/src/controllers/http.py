# -*- coding: utf-8 -*-

import asyncio

import aiohttp
from aiohttp.web_response import Response
from aiohttp.web_routedef import RouteTableDef
from dishka.integrations.aiohttp import FromDishka as Depends
from dishka.integrations.aiohttp import inject

from app.src.application.interactors import AddJsonInteractor, GetParsedDataInteractor
from app.src.config import RetriesConfig


router = RouteTableDef()


class Controllers:
    """
    Класс, содержащий контроллеры для обработки запросов.

    Methods:
        save_raw(config: Depends[RetriesConfig], interactor: Depends[AddJsonInteractor]) -> Response:
            Асинхронный метод для сохранения сырых данных с повторными попытками при ошибке.
        
        return_table(interactor: Depends[GetParsedDataInteractor]) -> Response:
            Асинхронный метод для получения и возврата обработанной таблицы.
    """

    @router.get('/save-json')
    @inject
    async def save_raw(
        self,
        config: Depends[RetriesConfig],
        interactor: Depends[AddJsonInteractor]
    ) -> Response:
        """
        Асинхронный метод для сохранения сырых данных с повторными попытками при ошибке.

        Args:
            config (Depends[RetriesConfig]): Конфигурация повторных попыток.
            interactor (Depends[AddJsonInteractor]): Взаимодействие для обработки JSON данных.

        Returns:
            Response: Ответ с результатом операции.
        """
        retry_attempts = 0
        while retry_attempts < config.max_retries:
            try:
                data = await interactor()
                return Response(
                    text=f'gateway data:\n{data}',
                    status=200
                )
            except aiohttp.ClientResponseError as exc:
                print(f"Error: {exc}")
                retry_attempts += 1
                if retry_attempts < config.max_retries:
                    wait_time = 2 ** retry_attempts
                    print(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    return Response(
                        text=f"Failed to fetch data after {config.max_retries} attempts",
                        status=500
                    )
        return Response(
            text="Unexpected error occurred",
            status=500
        )

    @router.get('/people')
    @inject
    async def return_table(
        self,
        interactor: Depends[GetParsedDataInteractor]
    ) -> Response:
        """
        Асинхронный метод для получения и возврата обработанной таблицы.

        Args:
            interactor (Depends[GetParsedDataInteractor]): Взаимодействие для получения и обработки данных.

        Returns:
            Response: Ответ с результатом операции.
        """
        try:
            data = await interactor()
            return Response(
                text=f'Data successfully executed\n{data}',
                status=200
            )
        except Exception as e:
            return Response(
                text=f"Failed to fetch data, error occurred:\n{e}",
                status=500
            )
