from fastapi import FastAPI
from app.routers import bookRoutes
from app.routers import user
from app.database.base import Base
from app.database.db import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API")

# Register routers

app.include_router(user.router) 
app.include_router(bookRoutes.router)

@app.get("/")
def root():
    return {"message": "Bookstore API running"}
