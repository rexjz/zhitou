import React, { useEffect, useMemo, useRef } from "react";

import { CopilotKit } from "@copilotkit/react-core";

import { WebSeachToolCallRenderer } from "@/components/ToolCall/web_search";
import { ThinkToolCallRenderer } from "@/components/ToolCall/think";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { Message, useAgent } from "@copilotkitnext/react";
// import { ActionExecutionMessage, ResultMessage, TextMessage } from "@copilotkit/runtime-client-gql";
import { useGetSessionMessages } from "@/sdk/agent/agent"

const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
};

const BasicChatPage: React.FC = () => {
  const sessionId = useMemo(() => {
    const params = new URLSearchParams(window.location.search);
    console.log("sessionId useMemo", params)
    const sessionFromUrl = params.get("sessionId");
    return sessionFromUrl || generateSessionId();
  }, []);
  console.log(sessionId)
  return (
    <CopilotKit
      runtimeUrl="/proxy/copilotkit"
      showDevConsole
      agent="default"
      headers={{
        "X-Agent-Session-ID": sessionId
      }}
      renderToolCalls={[
        WebSeachToolCallRenderer,
        ThinkToolCallRenderer
      ]}
      key={sessionId}
      threadId={sessionId}
    >
      <Chat sessionId={sessionId} />
    </CopilotKit>
  );
};

const Chat = ({ sessionId }: { sessionId: string }) => {

  const { agent } = useAgent({ agentId: "default" });

  const { data, isLoading } = useGetSessionMessages(sessionId)
  const hasLoadedHistory = useRef(false);

  useEffect(() => {
    if (!agent.isRunning && !isLoading && data && !hasLoadedHistory.current) {
      console.log(data.data)
      agent.setMessages(data?.data as any)
      hasLoadedHistory.current = true;
    }
  }, [agent, agent.isRunning, isLoading, data]);


  return (
    <div className="h-[calc(100vh-152px)] w-full rounded-lg">
      <CopilotChat
        className="h-full w-full rounded-lg"
        labels={{ initial: "你好，我有什么能帮你的？", placeholder: "在这里输入" }}
        suggestions="auto"
        hideStopButton
      />
    </div>
  );
};

export default BasicChatPage;
