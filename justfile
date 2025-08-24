start:
    uvicorn src.main:app --reload

database:
    uv run -m src.create_tables

create_migration:
    alembic revision --autogenerate -m "bootstrap schema"

perform_migration:
    alembic upgrade head

test:
    pytest --cov=src --cov-report=term-missing

check-ruff:
    ruff check .
    ruff format --check .

fix-ruff:
    ruff check . --fix
    ruff format .

pipeline: check-ruff test