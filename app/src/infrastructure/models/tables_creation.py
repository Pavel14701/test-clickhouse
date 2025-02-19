#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dishka import FromDishka as Depends, make_container
from sqlalchemy.orm import Session
import sqlalchemy as sa

from app.src.config import Config
from app.src.ioc import MigrationsProvider


def create_raw_table(session: Depends[Session]) -> None:
    """
    Создает таблицу raw_table в базе данных ClickHouse, если она не существует.

    Args:
        session (Depends[Session]): Сессия SQLAlchemy для выполнения запросов.
    """
    query = sa.text("""
        CREATE TABLE IF NOT EXISTS raw_table 
        (
            json_data String,
            hash UInt64 DEFAULT cityHash64(json_data),
            _inserted_at DateTime DEFAULT now()
        ) 
        ENGINE = ReplacingMergeTree(_inserted_at)
        ORDER BY hash;
    """)
    session.execute(statement=query)

def create_parsed_table(session: Depends[Session]) -> None:
    """
    Создает таблицу parsed_table в базе данных ClickHouse, если она не существует.

    Args:
        session (Depends[Session]): Сессия SQLAlchemy для выполнения запросов.
    """
    query = sa.text("""
        CREATE TABLE IF NOT EXISTS parsed_table
        (
            craft String,
            name String,
            _inserted_at DateTime DEFAULT now(),
            hash UInt64 DEFAULT cityHash64(craft || name)
        )
        ENGINE = ReplacingMergeTree(_inserted_at)
        ORDER BY hash;
    """)
    session.execute(statement=query)

def create_mv_raw_to_parsed(session: Depends[Session]) -> None:
    """
    Создает материализованное представление mv_raw_to_parsed в базе данных ClickHouse,
    если оно не существует, для преобразования данных из raw_table в parsed_table.

    Args:
        session (Depends[Session]): Сессия SQLAlchemy для выполнения запросов.
    """
    query = sa.text("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_raw_to_parsed
        TO parsed_table
        AS SELECT
            JSONExtractString(person, 'craft') AS craft,
            JSONExtractString(person, 'name') AS name
        FROM 
        (
            SELECT arrayJoin(JSONExtractArrayRaw(json_data, 'people')) AS person
            FROM raw_table
        ) 
        AS subquery;
    """)
    session.execute(statement=query)

def main():
    """
    Основная функция для инициализации конфигурации и создания таблиц и
    представлений в базе данных ClickHouse.
    """
    config = Config()
    container = make_container(MigrationsProvider(), context={Config: config})
    with container() as action:
        create_raw_table(action.get(Session))
        create_parsed_table(action.get(Session))
        create_mv_raw_to_parsed(action.get(Session))

if __name__ == "__main__":
    main()
