from typing import Annotated
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from fastapi import FastAPI, Header, Request, HTTPException, status
from zhitou_agent.agent.agno import create_agno_zhitou_agent


agui_app = FastAPI()

@agui_app.post("/agui-proxy")
async def agui_proxy(
  request: Request,
  x_agent_session_id: Annotated[
    str | None, Header(None, alias="X-Agent-Session-ID")
  ] = None,
  x_agent_user_id: Annotated[str | None, Header(None, alias="X-Agent-User-ID")] = None,
):
  if not x_agent_session_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Missing required header: X-Agent-Session-ID"
    )

  if not x_agent_user_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Missing required header: X-Agent-User-ID"
    )

  session_id = x_agent_session_id
  user_id = x_agent_user_id
  body = await request.json()
  body["forwarded_props"] = body.get("forwarded_props", {})
  body["forwarded_props"]["user_id"] = user_id
  # 让 threadId 保持一致或根据需要覆盖
  if session_id:
    body["thread_id"] = session_id

  # 生成一个 agent 实例，根据 session/user 来传参
  agent = create_agno_zhitou_agent(
    session_id=session_id or body.get("thread_id"),
    user_id=user_id,
  )

  agui_interface = AGUI(agent=agent)

  # 为这个请求临时创建一个 AgentOS 实例
  # 也可以 app.mount() 到某个子路径
  agent_os = AgentOS(agents=[agent], interfaces=[agui_interface])
  fastapi_app = agent_os.get_app()

  # 将当前请求转发到 AgentOS AG-UI 处理逻辑
  # 假设 AG-UI 端点是 /agui
  return await fastapi_app(request.scope, request.receive)
