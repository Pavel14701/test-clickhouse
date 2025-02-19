# -*- coding: utf-8 -*-

from typing import Generic

from aiohttp import ClientSession

from app.src.infrastructure.types import T


class SessionManager(Generic[T]):
    """
    Менеджер сессий для управления сессиями aiohttp.

    Attributes:
        sessions (list[ClientSession]): Список активных сессий.
    """

    def __init__(self):
        self.sessions: list[ClientSession] = []

    async def create_session(self) -> ClientSession:
        """
        Создает новую сессию aiohttp и добавляет ее в список сессий.

        Returns:
            ClientSession: Новая сессия aiohttp.
        """
        session = ClientSession()
        self.sessions.append(session)
        return session

    async def close_all_sessions(self) -> None:
        """
        Закрывает все активные сессии aiohttp и очищает список сессий.
        """
        for session in self.sessions:
            if not session.closed:
                await session.close()
        self.sessions = []


def new_request_session_maker() -> SessionManager[ClientSession]:
    """
    Создает новый менеджер сессий для aiohttp.

    Returns:
        SessionManager[ClientSession]: Новый менеджер сессий для aiohttp.
    """
    return SessionManager()
