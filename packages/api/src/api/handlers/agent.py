from typing import Annotated, Literal, Optional
from api.state import AppState, RequestState, get_app_state_dep, get_request_state_dep
from core.models.user import UserModel
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response, status
from api.middleware import get_current_user
from pydantic import BaseModel
from zhitou_agent.ag_ui.agui_app import create_agui_agno_app
from starlette.types import Scope, Receive, Send

# agent_app = APIRouter(dependencies=[Depends(get_current_user)], tags=["Agent"])
agent_app = APIRouter(tags=["Agent"])


class ASGIProxyResponse(Response):
  def __init__(self, app, scope: Scope, receive: Receive):
    super().__init__(content=b"")  # 占位，不会用到
    self._app = app
    self._scope = scope
    self._receive = receive

  async def __call__(self, scope: Scope, receive: Receive, send: Send):
    # 关键：不要拦截/拼接 body，直接让下游 app 用同一个 send
    await self._app(self._scope, self._receive, send)


@agent_app.post("/agui", operation_id="run agui agent")
async def agui_proxy(
  request: Request,
  current_user: UserModel = Depends(get_current_user),
  x_agent_session_id: Annotated[str | None, Header(alias="X-Agent-Session-ID")] = None,
):
  if not x_agent_session_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Missing required header: X-Agent-Session-ID",
    )

  agui_app = create_agui_agno_app(
    session_id=x_agent_session_id, user_id=str(current_user.id)
  )

  request.scope["path"] = "/agui"

  return ASGIProxyResponse(agui_app, request.scope, request.receive)


@agent_app.get("/status", operation_id="agui status")
async def status_proxy(
  request: Request,
  current_user: UserModel = Depends(get_current_user),
  x_agent_session_id: Annotated[str | None, Header(alias="X-Agent-Session-ID")] = None,
):
  if not x_agent_session_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Missing required header: X-Agent-Session-ID",
    )
  agui_app = create_agui_agno_app(
    session_id=x_agent_session_id, user_id=str(current_user.id)
  )

  request.scope["path"] = "/status"

  response_start = {}
  body_chunks = []

  async def send(message):
    if message["type"] == "http.response.start":
      response_start.update(message)
    elif message["type"] == "http.response.body":
      body_chunks.append(message.get("body", b""))

  await agui_app(request.scope, request.receive, send)

  headers = {
    k.decode("latin-1"): v.decode("latin-1")
    for k, v in response_start.get("headers", [])
  }

  return Response(
    content=b"".join(body_chunks),
    status_code=response_start["status"],
    headers=headers,
  )


@agent_app.get("/sessions", operation_id="get current user sessions")
async def get_current_user_sessions(
  current_user: UserModel = Depends(get_current_user),
  app_state: AppState = Depends(get_app_state_dep),
  # request_state: RequestState = Depends(get_request_state_dep),
  page_size: Optional[int] = 10,
  page_number: Optional[int] = 1,
  sort_order: Optional[Literal["desc", "asc"]] = "desc",
):
  sessions, total = app_state.repositories.agent_repo.get_sessions(
    user_id=str(current_user.id),
    page_size=page_size,
    page_number=page_number,
    sort_order=sort_order,
  )

  for session in sessions:
    session.pop("runs", None)
    session.pop("session_data", None)

  return {
    "sessions": sessions,
    "total": total,
    "page_size": page_size,
    "page_number": page_number,
  }

# class AgentSessionData(BaseModel):
#   title: str
#   messages: 

# @agent_app.get("/session/{session_id}", operation_id="get current session detail")
# async def get_current_user_sessions(