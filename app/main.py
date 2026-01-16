from fastapi import FastAPI
from app.routers import workflow_router
from app.routers import bookRoutes
from app.routers import user
from app.routers import order
from app.routers import paymentRoutes
from app.database.base import Base
from app.database.db import engine
from app.database.event import set_audit_fields




# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API")

# Register routers
app.include_router(paymentRoutes.router)
app.include_router(workflow_router.router)
app.include_router(order.router)
app.include_router(user.router) 
app.include_router(bookRoutes.router)


@app.get("/")
def root():
    return {"message": "Bookstore API running"}
