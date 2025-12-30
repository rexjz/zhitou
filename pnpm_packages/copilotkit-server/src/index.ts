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
    const init = super.requestInit(input);
    const dynamicHeaders = (input.forwardedProps?.forwardedHeaders) || {};
    return {
      ...init,
      headers: {
        ...init.headers,
        ...dynamicHeaders,  // 把你的 header 注入进去
      },
    };
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
    req.body.forwardedProps = {
      ...req.body.forwardedProps,
      forwardedHeaders: {
        Authorization: req.headers.authorization,
        "x-custom": req.headers["x-custom"],
      },
    };
    next();
  },
  copilotRuntimeNodeExpressEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/copilotkit"
  })
);

app.get("/health", (_req, res) => res.send("ok"));

app.listen(6010, () => {
  console.log("Listening on http://localhost:6010");
});
