## Litestar / SQLAlchemy CRUD пример

Проект реализует CRUD API для пользователей на базе Litestar и SQLAlchemy (async engine). Также включены миграции Alembic и вспомогательные скрипты для наполнения и просмотра данных.

### Требования
- Python 3.11+  
- PostgreSQL 14+ (локальный или доступный по сети)  
- `pip`/`venv` для установки зависимостей  
- Дополнительно для синхронных скриптов: драйвер `psycopg2-binary` (если не установлен)

### Быстрый старт
1) Клонировать репозиторий и перейти в папку проекта:
   - `git clone <url>`  
   - `cd Homework`
2) Создать и активировать виртуальное окружение:
   - Windows: `python -m venv .venv` и `.\.venv\Scripts\activate`
   - Linux/macOS: `python -m venv .venv` и `source .venv/bin/activate`
3) Установить зависимости API:
   - `pip install -r requirements.txt`
   - Если будете запускать скрипты `populate_*.py` или `query_data.py`, установите дополнительно `pip install psycopg2-binary`.
4) Настроить подключение к БД PostgreSQL:
   - Для API (async): переменная окружения `DATABASE_URL`, например  
     `postgresql+asyncpg://user:password@localhost:5432/dbname`
   - Для Alembic и вспомогательных скриптов (sync): обновите `config.py` и `alembic.ini` (параметр `sqlalchemy.url`) на строку вида  
     `postgresql+psycopg2://user:password@localhost:5432/dbname`
5) Применить миграции:
   - `alembic upgrade head`
6) Запустить API:
   - `uvicorn app.main:app --reload`
   - Приложение стартует на `http://localhost:8000`

### Основные эндпоинты
- `GET /users/{user_id}` — получить пользователя по ID  
- `GET /users?count=10&page=1&username=&email=` — список с пагинацией и фильтрами  
- `POST /users` — создать (тело: `username`, `email`, `description?`)  
- `PUT /users/{user_id}` — обновить данные  
- `DELETE /users/{user_id}` — удалить пользователя

### Наполнение и просмотр данных (не обязательно)
После применения миграций:
- `python populate_db.py` — создаёт пользователей и адреса  
- `python populate_products_orders.py` — создаёт продукты и заказы  
- `python query_data.py` — выводит пользователей и их адреса в консоль

### Полезные заметки
- В `app/main.py` указан fallback `DATABASE_URL`; для реального запуска используйте переменную окружения.  
- Миграции лежат в `migrations/versions`. Перед запуском убедитесь, что `alembic.ini` указывает на вашу БД.  
- Логи SQL включены (`echo=True`), отключите при необходимости.

### Структура проекта (кратко)
- `app/main.py` — инициализация Litestar и DI  
- `app/controllers/user_controller.py` — REST-эндпоинты  
- `app/services/user_service.py` — бизнес-логика  
- `app/repositories/user_repository.py` — работа с БД  
- `models.py` — модели SQLAlchemy  
- `migrations/` — Alembic миграции  
- `populate_db.py`, `populate_products_orders.py`, `query_data.py` — вспомогательные скрипты


