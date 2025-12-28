from typing import Annotated
from core.models.user import UserModel
from fastapi import Depends, FastAPI, HTTPException, Header, Request, status
from api.middleware import get_current_user
from zhitou_agent.ag_ui.agui_app import create_agui_agno_app

agent_app = FastAPI(dependencies=[Depends(get_current_user)])


@agent_app.post("/agui")
async def agui_proxy(
  request: Request,
  current_user: UserModel = Depends(get_current_user),
  x_agent_session_id: Annotated[
    str | None, Header(None, alias="X-Agent-Session-ID")
  ] = None,
):
  if not x_agent_session_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Missing required header: X-Agent-Session-ID",
    )
  agui_app = create_agui_agno_app(
    session_id=x_agent_session_id, user_id=str(current_user.id)
  )
  path = request.scope["path"]
  if "/agui" in path:
    agui_index = path.find("/agui")
    request.scope["path"] = path[agui_index:]
  return await agui_app(request.scope, request.receive)
