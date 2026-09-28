from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine, Base, init_db
from app.routers import user, listing, location, property_image, favorite, inquiry


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup, skipping if the database is unavailable."""
    try:
        await init_db()
    except Exception:
        pass
    yield


app = FastAPI(
    title="Real Estate Architecture",
    description="Independent Domain Driven Router Nodes for Real Estate Applications.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(user.router)
app.include_router(listing.router)
app.include_router(location.router)
app.include_router(property_image.router)
app.include_router(favorite.router)
app.include_router(inquiry.router)


@app.get("/")
async def root():
    return {"status": "fully_modular_architecture_online"}