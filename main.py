import asyncio

from fastapi import FastAPI, HTTPException, status, Depends
import uvicorn

from app.routes.users import users_route
from app.db.users.models import create_db


app = FastAPI()
app.include_router(users_route)



if __name__ == "__main__":
    asyncio.run(create_db())
    # uvicorn.run("main:app", reload=True)