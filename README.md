# Лабораторная работа: SQLAlchemy и Alembic

## Описание проекта

Этот проект демонстрирует работу с библиотеками SQLAlchemy и Alembic для создания и управления реляционными базами данных на Python.

## Структура проекта

```
lr2/
├── models.py                    # ORM модели (User, Address, Product, Order)
├── config.py                    # Конфигурация подключения к БД
├── populate_db.py               # Скрипт для наполнения БД пользователями и адресами
├── populate_products_orders.py  # Скрипт для наполнения БД продуктами и заказами
├── query_data.py               # Скрипт для запроса связанных данных
├── alembic.ini                 # Конфигурация Alembic
├── database.db                 # База данных SQLite (создается автоматически)
├── migrations/                 # Папка с миграциями
│   ├── env.py                  # Настройки окружения для миграций
│   └── versions/               # Файлы миграций
├── ANSWERS.md                  # Ответы на вопросы
└── README.md                   # Этот файл
```

## Что было сделано

### 1. Установка библиотек
- `sqlalchemy` - ORM для работы с базами данных
- `alembic` - система миграций базы данных
- `psycopg2-binary` - драйвер для PostgreSQL (для будущего использования)
- `asyncpg` - асинхронный драйвер для PostgreSQL (не установлен из-за требований компилятора)

### 2. Создание ORM моделей

#### Модель User (Пользователь)
- `id` - UUID, первичный ключ
- `username` - уникальное имя пользователя
- `email` - уникальный email
- `description` - дополнительное описание (добавлено позже)
- `created_at`, `updated_at` - временные метки

#### Модель Address (Адрес)
- `id` - UUID, первичный ключ
- `user_id` - внешний ключ на User
- `street`, `city`, `state`, `zip_code`, `country` - адресные данные
- `is_primary` - флаг основного адреса
- `created_at`, `updated_at` - временные метки

#### Модель Product (Продукт)
- `id` - UUID, первичный ключ
- `name` - название продукта
- `description` - описание
- `price` - цена (Decimal)
- `created_at`, `updated_at` - временные метки

#### Модель Order (Заказ)
- `id` - UUID, первичный ключ
- `user_id` - внешний ключ на User
- `delivery_address_id` - внешний ключ на Address
- `total_amount` - общая сумма заказа
- `status` - статус заказа (pending, processing, shipped, delivered)
- `created_at`, `updated_at` - временные метки

### 3. Типы связей между таблицами

1. **Один-ко-многим (One-to-Many)**:
   - User → Address (один пользователь, много адресов)
   - User → Order (один пользователь, много заказов)
   - Address → Order (один адрес, много заказов)

2. **Многие-к-одному (Many-to-One)**:
   - Address → User (много адресов, один пользователь)
   - Order → User (много заказов, один пользователь)
   - Order → Address (много заказов, один адрес доставки)

3. **Многие-ко-многим (Many-to-Many)**:
   - Order ↔ Product (через промежуточную таблицу `order_product`)

### 4. Инициализация и настройка Alembic

1. Инициализирована папка миграций: `alembic init migrations`
2. Настроен `alembic.ini` с строкой подключения к БД
3. Настроен `migrations/env.py` для использования `Base.metadata`

### 5. Создание и применение миграций

1. **Первая миграция**: Создание таблиц `users` и `addresses`
2. **Вторая миграция**: Добавление поля `description` к `User`, создание таблиц `products`, `orders` и `order_product`

### 6. Наполнение базы данных

- **5 пользователей** с их адресами (через `populate_db.py`)
- **5 продуктов** (ноутбук, смартфон, наушники, планшет, умные часы)
- **5 заказов** с различными комбинациями продуктов

### 7. Запрос связанных данных

Реализован запрос с использованием `selectinload` для эффективной загрузки связанных данных:
```python
select(User).options(selectinload(User.addresses))
```

Это позволяет избежать проблемы N+1 запросов.

## Как использовать

### 1. Установка зависимостей
```bash
pip install sqlalchemy alembic psycopg2-binary
```

### 2. Настройка базы данных
Отредактируйте `config.py` или `alembic.ini` для настройки подключения к вашей БД.

По умолчанию используется SQLite (`sqlite:///./database.db`).

Для PostgreSQL:
```python
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"
```

### 3. Применение миграций
```bash
python -m alembic upgrade head
```

### 4. Наполнение базы данных
```bash
python populate_db.py              # Пользователи и адреса
python populate_products_orders.py # Продукты и заказы
```

### 5. Запрос данных
```bash
python query_data.py
```

### 6. Создание новой миграции
```bash
python -m alembic revision --autogenerate -m "Описание изменений"
python -m alembic upgrade head
```

