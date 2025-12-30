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
