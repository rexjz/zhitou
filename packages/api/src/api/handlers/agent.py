from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from ag_ui.core import (
  RunAgentInput,
  RunStartedEvent,
  TextMessageStartEvent,
  TextMessageContentEvent,
  StateDeltaEvent,
  TextMessageEndEvent,
  RunFinishedEvent,
)
from ag_ui.encoder import EventEncoder
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.plan import PlanNotebook, Plan, SubTask
import openai
import os
import asyncio
from agentscope.agent import ReActAgent
from zhitou_agent.memory.TruncatableMemory import TruncatableMemory
from zhitou_agent.tools.bocha_web_search import BoChaTools
from agentscope.tool import Toolkit
from zhitou_agent.prompt.system import system_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AG-UI Chat SSE Server")


def _create_agent(
  bocha_apikey: str, dashscpope_apikey: str, pre_print_hook_function: callable
):
  plan_notebook = PlanNotebook()
  toolkit = Toolkit()
  bocha_tools = BoChaTools(apikey=bocha_apikey)
  toolkit.register_tool_function(bocha_tools.bocha_web_search)

  agent = ReActAgent(
    name="zhitou_agent",
    sys_prompt=system_prompt,
    model=DashScopeChatModel(
      model_name="qwen-max",
      api_key=dashscpope_apikey,
      stream=True,
    ),
    memory=TruncatableMemory(),
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    plan_notebook=plan_notebook,
  )

  agent.register_instance_hook("pre_print", "forward_print", pre_print_hook_function)

  return agent


@app.post("/agui-chat")
async def agui_chat(request: Request):
  """
  AG-UI 兼容的 SSE 端点：

  - 前端会 POST RunAgentInput JSON
  - 后端基于模型或逻辑逐 token 生成响应
  - 推送 AG-UI 事件消息到客户端 SSE
  """

  

  input_data: RunAgentInput = await request.json()
  encoder = EventEncoder()

  async def event_generator():
    # run started 事件
    yield encoder.encode(
      RunStartedEvent(thread_id=input_data.thread_id, run_id=input_data.run_id)
    )

    # 发送 message start 事件
    yield encoder.encode(TextMessageStartEvent(role="assistant"))

    # 调用 OpenAI ChatCompletion API，并逐 token 推送
    completion = openai.ChatCompletion.create(
      model="gpt-4o-mini",
      messages=[{"role": m.role, "content": m.content} for m in input_data.messages],
      stream=True,
    )
    StateDeltaEvent()
    async for chunk in completion:
      # chunk['choices'][0]['delta'] 可能包含 content
      text = chunk["choices"][0].get("delta", {}).get("content")
      if text:
        yield encoder.encode(TextMessageContentEvent(data=text))

      await asyncio.sleep(0)  # 允许事件循环轮转

    # message end
    yield encoder.encode(TextMessageEndEvent())

    # run finished
    yield encoder.encode(RunFinishedEvent())

  return StreamingResponse(
    event_generator(),
    media_type="text/event-stream",
  )


# 运行服务： uvicorn main:app --reload --host 0.0.0.0 --port 8000
