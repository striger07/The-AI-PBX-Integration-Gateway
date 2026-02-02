from fastapi import FastAPI
from app.api.v1.routes_call import router
from app.core.database import engine, Base

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
