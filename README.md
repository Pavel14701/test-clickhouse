# Проект Test Clickhouse выполнение тестового 

### Содержание
1. *[Введение](README.md)*

2. [Техническое задание](docs/2_specification.md)

3. [Архитектура проекта](docs/3_architecture.md)

4. [Быстрый старт](docs/4_quick_start.md)

5. [Маршруты](docs/5_routes.md)


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