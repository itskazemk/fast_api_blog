import uvicorn

from db.engine import Base, engine
from fastapi import FastAPI
from routers.users import router as user_router

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router, prefix="/user")


if __name__ == "__main__":
    uvicorn.run(app)
