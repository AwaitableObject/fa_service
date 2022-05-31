from typing import Tuple

from fastapi import APIRouter

from app.api.endpoints.allocations import router as allocations_router

ROUTERS: Tuple[APIRouter] = (allocations_router,)
