from fastapi import FastAPI


app = FastAPI()

"""Only uncomment below to create new tables"""
# Base.metadata.create_all(bind=engine)
