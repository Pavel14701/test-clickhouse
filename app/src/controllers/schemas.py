# -*- coding: utf-8 -*-

from datetime import datetime

from pydantic import BaseModel, Field


class RawJsonSchema(BaseModel):
    """
    Схема для валидации необработанных данных JSON из ClickHouse.

    Attributes:
        data (str): Необработанные данные JSON.
        hash (int): Хеш-значение данных.
        inserted_at (datetime): Время вставки данных.
    """
    data: str = Field(alias='json_data')
    hash: int
    inserted_at: datetime = Field(alias='_inserted_at')

    class Config:
        populate_by_name = True


class AstronautSchema(BaseModel):
    """
    Схема для валидации данных об астронавтах из ClickHouse.

    Attributes:
        name (str): Имя астронавта.
        craft (str): Космический корабль, на котором находится астронавт.
        hash (int): Хеш-значение данных.
        inserted_at (datetime): Время вставки данных.
    """
    name: str
    craft: str
    hash: int
    inserted_at: datetime = Field(alias='_inserted_at')

    class Config:
        populate_by_name = True
