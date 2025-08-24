from src.database.core import Base, engine

Base.metadata.create_all(bind=engine)
