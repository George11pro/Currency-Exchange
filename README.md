# Currency Exchange API

REST API для работы с валютами и обменными курсами.

Приложение позволяет:

- получать список валют;
- получать информацию о конкретной валюте;
- добавлять новые валюты;
- получать список обменных курсов;
- получать конкретный обменный курс;
- добавлять обменные курсы;
- изменять существующие обменные курсы;
- рассчитывать конвертацию произвольной суммы между валютами.

Веб-интерфейс для проекта не предусмотрен.

## Технологии

- Python 3.12+
- FastAPI
- Uvicorn
- SQLite
- Pydantic
- pytest

## Структура проекта

``` text
Currency_Exchange/
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── currency_exchange.db
│
├── repositories/
│   ├── __init__.py
│   ├── currency_repository.py
│   └── exchange_rate_repository.py
│
├── routers/
│   ├── __init__.py
│   ├── currencies.py
│   └── exchange_rates.py
│
├── schemas/
│   ├── __init__.py
│   ├── currency.py
│   └── exchange_rate.py
│
├── services/
│   ├── __init__.py
│   ├── currency_service.py
│   └── exchange_rate_service.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_currencies.py
│   ├── test_exchange.py
│   └── test_exchange_rates.py
│
├── utils/
│   └── validators.py
│
├── main.py
├── requirements.txt
└── README.md

```


Установка
Клонировать проект и перейти в его директорию:

cd Currency_Exchange

Создать виртуальное окружение:

python -m venv .venv

Активировать виртуальное окружение.

Windows
.venv\Scripts\activate

Linux
source .venv/bin/activate

Установить зависимости:

pip install -r requirements.txt

Запуск приложения
Запустить сервер командой:

python --m uvicorn main:app --reload --host 127.0.0.1 --port 8000

Запуск фронтенда:

docker start currency-exchange-frontend-nginx

После запуска приложение(фронтенд xfcnm) доступно для теста на http://localhost

Интерактивная документация Swagger:

http://127.0.0.1:8000/docs

Также доступна документация ReDoc:

http://127.0.0.1:8000/redoc

API
Валюты
Получить список валют
GET /currencies

Пример ответа:

[
    {
        "id": 1,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    {
        "id": 2,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
]

Получить валюту
GET /currency/{code}

Пример:

GET /currency/USD

Добавить валюту
POST /currencies

Формат данных:

name=Euro
code=EUR
sign=€

Используется application/x-www-form-urlencoded.

Пример ответа:

{
    "id": 2,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}

Обменные курсы
Получить все обменные курсы
GET /exchangeRates

Получить обменный курс
GET /exchangeRate/{pair}

Пример:

GET /exchangeRate/USDEUR

Добавить обменный курс
POST /exchangeRates

Формат данных:

baseCurrencyCode=USD
targetCurrencyCode=EUR
rate=0.92

Используется application/x-www-form-urlencoded.

Изменить обменный курс
PATCH /exchangeRate/{pair}

Пример:

PATCH /exchangeRate/USDEUR

Данные:

rate=0.95

Конвертация валют
GET /exchange?from=USD&to=EUR&amount=100

Пример ответа:

{
    "baseCurrency": {
        "id": 1,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 2,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.92,
    "amount": 100,
    "convertedAmount": 92
}

Для определения курса используются следующие варианты:

Прямой курс A -> B.

Обратный курс B -> A с расчётом обратного значения.

Расчёт через USD.

Коды HTTP
API использует стандартные HTTP-коды:

Код	Назначение
200	Успешный запрос
201	Ресурс создан
400	Некорректные данные запроса
404	Ресурс не найден
409	Конфликт данных
500	Внутренняя ошибка сервера

При ошибках API возвращает JSON следующего вида:

{
    "message": "Валюта не найдена"
}

База данных
Для хранения данных используется SQLite.

Файл базы данных:

database/currency_exchange.db

Используются две таблицы:

Currencies
Поле	Описание
ID	Первичный ключ
Code	Код валюты
FullName	Полное название валюты
Sign	Символ валюты

ExchangeRates
Поле	Описание
ID	Первичный ключ
BaseCurrencyId	ID базовой валюты
TargetCurrencyId	ID целевой валюты
Rate	Обменный курс

Для валют действует уникальность по Code.

Для обменных курсов действует уникальность по паре:

BaseCurrencyId + TargetCurrencyId

Тестирование
Для запуска тестов используется pytest:

pytest

Тесты проверяют:

- получение валют;

- создание валют;

- обработку дубликатов;

- обработку неизвестных валют;

- получение обменных курсов;

- создание обменных курсов;

- обновление обменных курсов;

- обработку некорректных курсов;

- конвертацию валют;

расчёт курса через обратную валютную пару;

расчёт курса через USD.

Архитектура
Проект разделён на несколько уровней:

Router
   ↓
Service
   ↓
Repository
   ↓
SQLite

Routers
Обрабатывают HTTP-запросы и HTTP-ответы.

Services
Содержат бизнес-логику приложения.

Repositories
Отвечают за взаимодействие с SQLite.

Schemas
Описывают структуру ответов API с помощью Pydantic.

Utils
Содержит вспомогательные функции, например валидацию кодов валют и валютных пар.

Запуск без режима разработки
Для запуска приложения без автоматической перезагрузки:

uvicorn main:app

Для запуска на всех сетевых интерфейсах:

uvicorn main:app --host 0.0.0.0 --port 8000

В таком случае API будет доступно на порту 8000.

Лицензия
Учебный проект.