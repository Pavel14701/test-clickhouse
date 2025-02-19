Техническое задание
===================

В этом разделе представлено техническое задание для проекта Test Clickhouse.

## Общие сведения

Проект Test Clickhouse предназначен для работы с базой данных Clickhouse. Он включает следующие модули и компоненты:

- `application`: Основная логика приложения
- `config`: Конфигурация проекта
- `controllers`: Контроллеры для обработки HTTP-запросов
- `infrastructure`: Инфраструктурные компоненты, такие как работа с базой данных
- `main`: Точка входа в приложение
- `ioc`: Создание DI контейнеров
## Требования

- Python 3.12
- Poetry для управления зависимостями

## Архитектура

Проект организован в виде модулей и пакетов, как показано ниже:



Структура проекта
=================
```
app
├── src
│   ├── application
│   │   ├── __init__.py
│   │   ├── interactors.py
│   │   ├── interfaces.py
│   ├── config.py
│   ├── controllers
│   │   ├── http.py
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── infrastructure
│   │   ├── database.py
│   │   ├── gateways.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── tables_creation.py
│   │   ├── request.py
│   │   └── types.py
│   ├── ioc.py
│   └── main.py
├── docker_config
│   ├── config.xml
│   ├── run_container.sh
│   ├── create_image.sh
│   ├── supervisord.conf
│   └── users.xml
├── poetry.lock
├── pyproject.toml
├── README.md
├── run_table_creation.sh
└── run_app.sh
```

### Содержание
1. [Введение](../README.md)

2. [Техническое задание](2_specification.md)

3. *[Архитектура проекта](3_architecture.md)*

4. [Быстрый старт](4_quick_start.md)

5. [Маршруты](5_routes.md)
