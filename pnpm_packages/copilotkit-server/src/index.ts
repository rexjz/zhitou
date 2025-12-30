import express from "express";
import {
  CopilotRuntime,
  copilotRuntimeNodeExpressEndpoint,
  ExperimentalEmptyAdapter
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";

const app = express();
app.use(express.json());

const aguiAgent = new HttpAgent({
  url: "http://localhost:6008/api/agent/agui",
  agentId: "default"
});

const runtime = new CopilotRuntime({
  agents: { default: aguiAgent }
});
const serviceAdapter = new ExperimentalEmptyAdapter();

app.post(
  "/copilotkit",
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
