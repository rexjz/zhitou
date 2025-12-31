from fastapi import APIRouter
from api.api_models.api_response import APIResponse
from fastapi.responses import StreamingResponse
import json
import time
import asyncio


system_router = APIRouter(tags=["System"])


@system_router.get("/health")
def health():
  return APIResponse(message="ok")


@system_router.get("/")
def root():
  return "ok"


async def a_fake_json_streamer():
  print("a_fake_json_streamer")
  t0 = time.time()
  for i in range(10):
    print(f"Chunk being yielded (time {int((time.time() - t0) * 1000)}ms)", flush=True)
    yield json.dumps({"message": "Hello World"}) + "\n"
    await asyncio.sleep(0.5)
  print(f"Over (time {int((time.time() - t0) * 1000)}ms)", flush=True)


@system_router.get("/a_fake_json_streamer")
async def test1():
  return StreamingResponse(a_fake_json_streamer(), media_type="text/event-stream")


@system_router.post("/a_fake_json_streamer")
async def test2():
  return StreamingResponse(a_fake_json_streamer(), media_type="text/event-stream")


def fake_json_streamer():
  print("fake_json_streamer")
  t0 = time.time()
  for i in range(10):
    print(f"Chunk being yielded (time {int((time.time() - t0) * 1000)}ms)", flush=True)
    yield json.dumps({"message": "Hello World"}) + "\n"
    time.sleep(0.5)
  print(f"Over (time {int((time.time() - t0) * 1000)}ms)", flush=True)


@system_router.get("/fake_json_streamer")
async def test3():
  return StreamingResponse(fake_json_streamer(), media_type="text/event-stream")


@system_router.post("/fake_json_streamer")
async def test4():
  return StreamingResponse(fake_json_streamer(), media_type="text/event-stream")
