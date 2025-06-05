REST API для управления каталогом книг с возможностью хранения, редактирования и обогащения данных из внешнего источника (OpenLibrary API).

---

## Возможности

- CRUD-операции над книгами
- Хранение в PostgreSQL через SQLAlchemy
- Миграции с Alembic
- Обогащение данных (обложка, описание) через OpenLibrary API
- Конфигурация через .env
- Документация Swagger/OpenAPI
- Docker + Docker Compose
- Логирование (Loguru)
- pre-commit хуки: black, isort, flake8

---

## Модель книги

| Поле         | Тип        | Описание                 |
|--------------|------------|--------------------------|
| id           | int        | Уникальный идентификатор |
| title        | str        | Название книги           |
| author       | str        | Автор                    |
| year         | int        | Год издания              |
| genre        | str        | Жанр                     |
| pages        | int        | Кол-во страниц           |
| available    | bool       | В наличии / выдана       |

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-username/book-catalog-api.git
cd book-catalog-api

### 2. Настроить .env
```env
DATABASE_URL=postgresql://user:password@db:5432/books
LOG_LEVEL=INFO

### 3. Запуск через Docker Compose
```bash
docker-compose up --build

### 4. Применить миграции
docker exec -it <container_name> poetry run alembic upgrade head
