start:
    uvicorn src.main:app --reload

database:
    uv run -m src.create_tables