from fastapi import FastAPI

from app.api.endpoints import ROUTERS

app = FastAPI()

for router in ROUTERS:
    app.include_router(router)
