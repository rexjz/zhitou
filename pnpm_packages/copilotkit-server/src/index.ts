import express from "express";
import {
  CopilotRuntime,
  copilotRuntimeNodeExpressEndpoint,
  ExperimentalEmptyAdapter
} from "@copilotkit/runtime";
import { HttpAgent, type RunAgentInput } from "@ag-ui/client";
import cors from "cors";

const app = express();
app.use(express.json());
app.use(cors({
  origin: "http://localhost:6009",
}));

class DynamicHeaderAgent extends HttpAgent {
  protected requestInit(input: RunAgentInput) {
    const dynamicHeaders = (input.forwardedProps?.forwardedHeaders) || {};

    delete input.forwardedProps?.forwardedHeaders
    const init = super.requestInit(input);
 
    const request: any = {
      ...init,
      headers: {
        ...init.headers,
        ...dynamicHeaders,  // 把你的 header 注入进去
        "Accept-Encoding": "identity",
      },
    };
    console.log(request)


    console.log(JSON.stringify(request, null, 2))
    return request
  }
}

const aguiAgent = new DynamicHeaderAgent({
  url: "http://localhost:6008/api/agent/agui",
  agentId: "default"
});

const runtime = new CopilotRuntime({
  agents: { default: aguiAgent }
});
const serviceAdapter = new ExperimentalEmptyAdapter();

app.post(
  "/copilotkit",
  (req: any, res, next) => {
    console.log("req.headers: ", req.headers)
    // // 关键：告诉任何中间层别对内容做 transform（包括压缩/转码）
    // res.setHeader("Cache-Control", "no-cache, no-transform");
    // res.setHeader("Content-Type", "text/event-stream; charset=utf-8");
    // res.setHeader("Connection", "keep-alive");
    // res.setHeader("Content-Encoding", "");
    // res.setHeader("X-Accel-Buffering", "no");

    // // 有些代理/中间件会参考它；有也不吃亏
    // res.removeHeader("Content-Encoding");

    // res.flushHeaders?.();

    if(req.body.body) {

      const forwardedHeaders: any = {
        Cookie: req.headers.cookie // 如果你永远要加 Cookie
      };

      if (req.headers['x-agent-session-id']) {
        forwardedHeaders['X-Agent-Session-ID'] = req.headers['x-agent-session-id'];
      }

      req.body.body.forwardedProps = {
        ...req.body.body.forwardedProps,
        forwardedHeaders: forwardedHeaders,
      };
    } 
    next();
  },
  copilotRuntimeNodeExpressEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/copilotkit"
  })
);

app.get("/health", (_req, res) => res.send("ok"));

app.listen(6010, "0.0.0.0", () => {
  console.log("Listening on 6010");
});
