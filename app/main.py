from fastapi import FastAPI
from database import engine, Base
from app.routers import user, listing, location, property_image, favorite, inquiry

app = FastAPI(
    title="Real Estate Architecture",
    description="Independent Domain Driven Router Nodes for Real Estate Applications.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user.router)
app.include_router(listing.router)
app.include_router(location.router)
app.include_router(property_image.router)
app.include_router(favorite.router)
app.include_router(inquiry.router)

@app.get("/")
async def root():
    return {"status": "fully_modular_architecture_online"}
