"""
Конфигурация подключения к базе данных
"""
import os

# Для PostgreSQL используйте формат:
# DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"

# Для SQLite (для демонстрации и разработки):
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Для PostgreSQL раскомментируйте и настройте:
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"

