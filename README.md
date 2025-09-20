## 🍕 Pizza Store
API для пиццерии.
Реализован FastAPI сервис, который работает с PostgreSQL через SQLAlchemy ORM.
Поддерживается in-memory база для тестирования, бизнес-логика вынесена в отдельный слой (PizzaService).

## 🚀 Возможности
- Создание пользователя
- Создание заказа
- Добавление/удаление пиццы в заказ
- Обновление адреса доставки
- Расчёт цены заказа
- Управление статусами заказа (NEW → ORDERED → PREPARING → READY → DELIVERING → DELIVERED → COMPLETED)
- API-эндпоинты с валидацией через Pydantic

## 📦 Установка и запуск
1. Клонирование репозитория
   
`git clone https://github.com/Tar8117/pizza-store.git`

`cd pizza-store -> cd src`

3. Создание и активация виртуального окружения
   
`python -m venv venv`

#### Linux/Mac

`source venv/bin/activate` 

#### Windows

`venv\Scripts\activate`     

5. Установка зависимостей
`pip install -r requirements.txt`

## Настройка базы данных

В файле config.py укажите ваши параметры подключения к PostgreSQL:

`DB_SYNC_URL = "postgresql+psycopg2://postgres:password@localhost:5432/pizza_db"`

`DB_ASYNC_URL = "postgresql+asyncpg://postgres:password@localhost:5432/pizza_db"`

Создайте базу данных (через psql):

`createdb pizza_db`

## Создание таблиц

`python main.py`

## Запуск приложения
   
`uvicorn main_api:app --reload`

либо

`python main_api.py`


Приложение будет доступно по адресу:
👉 `http://127.0.0.1:8000`

Документация Swagger:
👉 `http://127.0.0.1:8000/docs`

## 🧪 Тесты

Тесты используют pytest и in-memory базу. Запуск:

`pytest test/test_pizza_service.py`

`pytest test/test_pizza_service_orm.py`
