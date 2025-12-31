import uuid
from typing import cast

from api.state import AppState, RequestState
from starlette.types import ASGIApp, Scope, Receive, Send, Message
from starlette.requests import Request


class RequestStateMiddleware:
  def __init__(self, app: ASGIApp):
    self.app = app

  async def __call__(self, scope: Scope, receive: Receive, send: Send):
    if scope["type"] != "http":
      return await self.app(scope, receive, send)

    request = Request(scope, receive=receive)

    app_state = cast(AppState, request.app.state.state)
    request_id = str(uuid.uuid4())
    session = app_state.db_manager.get_session()

    request.state.r_state = RequestState(db_session=session, request_id=request_id)

    async def send_wrapper(message: Message):
      if message["type"] == "http.response.start":
        headers = list(message.get("headers", []))
        headers.append((b"x-request-id", request_id.encode()))
        message["headers"] = headers
      await send(message)

    try:
      await self.app(scope, receive, send_wrapper)
    finally:
      # 如果你的 session 需要关闭/回收，一定别忘了
      try:
        session.close()
      except Exception:
        pass
