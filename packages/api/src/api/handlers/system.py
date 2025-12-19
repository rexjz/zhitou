from fastapi import APIRouter
from api.api_models.api_response import APIResponse

system_router = APIRouter(tags=["System"])


@system_router.get("/health")
def health():
  return APIResponse(message="ok")


@system_router.get("/")
def root():
  return "ok"
