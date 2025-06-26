import asyncio

from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

from app.routes.users import users_route
from app.db.base import create_db
from app.routes.products import products_route



app = FastAPI()
app.include_router(users_route)
app.include_router(products_route)
# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, ["127.0.0.1", "127.0.0.2", "127.0.0.3"])
app.add_middleware(GZipMiddleware, minimum_size=1000)








if __name__ == "__main__":
    # asyncio.run(create_db())
    uvicorn.run("main:app", reload=True)