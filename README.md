# Проект Test Clickhouse выполнение тестового 

## Содержание
1. [Введение](docs/1_introduction.md)

2. [Установка и настройка](docs/2_setup.md)

3. [Техническое задание](docs/3_specification.md)

4. [Архитектура проекта](docs/4_architecture.md)

5. [Структура проекта](docs/5_project_structure.md)

6. [Быстрый старт](docs/6_quick_start.md)

7. [Маршруты](docs/7_routes.md)


Этот проект демонстрирует работу с Clickhouse, используя Python для загрузки данных, их обработки и визуализации. Следуйте шагам, описанным ниже, для настройки и запуска проекта.

## Используемые пакеты

В проекте используются следующие пакеты:

- **python**: Язык программирования Python версии 3.12.
- **pydantic**: Используется для валидации данных и управления настройками через Python-классы.
- **sqlalchemy**: ORM для работы с базами данных. Обеспечивает удобное взаимодействие с базой данных Clickhouse.
- **clickhouse-driver**: Драйвер для подключения к Clickhouse и выполнения запросов.
- **clickhouse-sqlalchemy**: Интеграция SQLAlchemy с Clickhouse, что позволяет использовать ORM для работы с Clickhouse.
- **aiohttp**: Асинхронная библиотека для выполнения HTTP-запросов. Используется для повышения производительности при взаимодействии с внешними сервисами.
- **dishka**: Библиотека для работы с DI.
- **tabulate**: Библиотека для представления данных в табличном формате.