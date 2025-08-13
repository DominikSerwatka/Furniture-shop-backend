start:
    uvicorn src.main:app --reload

database:
    uv run -m src.create_tables

create_migration:
    alembic revision --autogenerate -m "bootstrap schema"

perform_migration:
    alembic upgrade head
