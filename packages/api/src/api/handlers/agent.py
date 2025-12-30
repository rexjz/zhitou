from typing import Annotated
from core.models.user import UserModel
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response, status
from api.middleware import get_current_user
from zhitou_agent.ag_ui.agui_app import create_agui_agno_app
from loguru import logger
agent_app = APIRouter(dependencies=[Depends(get_current_user)], tags=["Agent"])


@agent_app.post("/agui", operation_id="run agui agent")
async def agui_proxy(
  path: str,
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
  # logger.info(agui_app.routes)
  

  # path = f"/agui/{path}"
  request.scope["path"] = "/agui"

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


@agent_app.post("/proxy/copilotkit")
async def proxy_mixed(request: Request):
    # 读取原始请求体
    body = await request.body()

    # 构造转发 headers（剥离 Host 避免冲突）
    forward_headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() != "host"
    }

    async with httpx.AsyncClient(timeout=None) as client:
        # 发起流式请求（stream=True 保证可以实时读取）
        upstream_resp = await client.post(
            TARGET_URL,
            content=body,
            headers=forward_headers,
            params=request.query_params,
            stream=True,
        )

        # 判断响应是否 SSE
        content_type = upstream_resp.headers.get("content-type", "")

        # SSE 情况（EventSource/text event-stream）
        if "text/event-stream" in content_type:
            async def stream_iter():
                # 一边从上游读一边 Yield chunk
                async for chunk in upstream_resp.aiter_bytes():
                    yield chunk
                # 注意流结束后自动 close client
            return StreamingResponse(
                stream_iter(),
                media_type="text/event-stream"
            )

        # 非 SSE 情况 —— 普通读取 body 然后返回
        data = await upstream_resp.aread()
        headers = {
            k: v
            for k, v in upstream_resp.headers.items()
            # 过滤掉某些不适合转发给客户端的头
            if k.lower() not in {"content-encoding", "transfer-encoding", "connection"}
        }

        # 根据上游返回的 content-type 决定用 JSONResponse 或普通 Response
        if "application/json" in content_type:
            return JSONResponse(content=data, status_code=upstream_resp.status_code, headers=headers)
        else:
            return Response(content=data, status_code=upstream_resp.status_code, headers=headers)