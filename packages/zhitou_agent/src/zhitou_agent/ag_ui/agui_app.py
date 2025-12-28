from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from zhitou_agent.agent.agno import create_agno_zhitou_agent
from zhitou_agent.config import ZhitouAgentConfigLoader


def create_agui_agno_app(session_id, user_id):
  config = ZhitouAgentConfigLoader().load()

  agent = create_agno_zhitou_agent(
    session_id=session_id,
    user_id=user_id,
    bocha=config.bocha,
    dashscpope=config.dashscpope
  )
  agui_interface = AGUI(agent=agent)
  agent_os = AgentOS(agents=[agent], interfaces=[agui_interface])
  return agent_os.get_app()