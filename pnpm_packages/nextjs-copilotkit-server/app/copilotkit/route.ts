import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { AgnoAgent } from "@ag-ui/agno";
import { NextRequest } from "next/server";

class DynamicHeaderAgent extends AgnoAgent {
  protected requestInit(input: any) {
    const dynamicHeaders = (input.forwardedProps?.forwardedHeaders) || {};

    delete input.forwardedProps?.forwardedHeaders;
    const init = super.requestInit(input);

    const request: any = {
      ...init,
      headers: {
        ...init.headers,
        ...dynamicHeaders
      },
    };
    console.log(request);

    console.log(JSON.stringify(request, null, 2));
    return request;
  }
}

const serviceAdapter = new ExperimentalEmptyAdapter();

const aguiAgent = new DynamicHeaderAgent({
  url: "http://localhost:6008/api/agent/agui",
  agentId: "default"
});

const runtime = new CopilotRuntime({
  agents: { default: aguiAgent }
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/copilotkit",
  });

  // Clone the request and modify the body
  const body = await req.json();

  if (body.body) {
    const forwardedHeaders: any = {
      Cookie: req.headers.get('cookie')
    };

    if (req.headers.get('x-agent-session-id')) {
      forwardedHeaders['X-Agent-Session-ID'] = req.headers.get('x-agent-session-id');
    }

    body.body.forwardedProps = {
      ...body.body.forwardedProps,
      forwardedHeaders: forwardedHeaders,
    };
  }

  // copilitkit always sends full messages, this is a workaround
  if (body?.method === "agent/run" && Array.isArray(body.body?.messages) && body.body.messages.length > 1) {
    body.body.messages = [body.body.messages[body.body.messages.length - 1]];
  }

  // Create a new request with the modified body
  const modifiedReq = new Request(req.url, {
    method: req.method,
    headers: req.headers,
    body: JSON.stringify(body),
  }) as NextRequest;

  return handleRequest(modifiedReq);
};