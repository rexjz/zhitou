import React, { useEffect, useRef, useState } from "react";

import { CopilotKit } from "@copilotkit/react-core";

import { WebSeachToolCallRenderer } from "@/components/ToolCall/web_search";
import { ThinkToolCallRenderer } from "@/components/ToolCall/think";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { useAgent } from "@copilotkitnext/react";
// import { ActionExecutionMessage, ResultMessage, TextMessage } from "@copilotkit/runtime-client-gql";
import { useGetSessionMessages } from "@/sdk/agent/agent";
import SessionListView from "@/components/AgentChat/SessionListView";
import type { SessionData } from "@/sdk/models/sessionData";

const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
};

const BasicChatPage: React.FC = () => {
  const [currentSessionId, setCurrentSessionId] = useState<string>(() => {
    const params = new URLSearchParams(window.location.search);
    const sessionFromUrl = params.get("sessionId");
    return sessionFromUrl || generateSessionId();
  });

  const handleSessionClick = (session: SessionData) => {
    setCurrentSessionId(session.session_id);
    // Update URL without page reload
    const url = new URL(window.location.href);
    url.searchParams.set("sessionId", session.session_id);
    window.history.pushState({}, "", url.toString());
  };

  return (
    <div className="h-[calc(100vh-152px)] flex">
      {/* Session List Sidebar */}
      <div style={{
        width: "320px",
        borderRight: "1px solid #f0f0f0",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column"
      }}>
        <div style={{
          padding: "16px",
          borderBottom: "1px solid #f0f0f0",
          fontWeight: "bold",
          fontSize: "16px"
        }}>
          历史会话
        </div>
        <div style={{ flex: 1, overflow: "hidden" }}>
          <SessionListView
            activatedSessionId={currentSessionId}
            onSessionClick={handleSessionClick}
          />
        </div>
      </div>

      {/* Chat Area */}
      <div style={{ flex: 1, overflow: "hidden" }}>
        <CopilotKit
          runtimeUrl="/proxy/copilotkit"
          showDevConsole
          agent="default"
          headers={{
            "X-Agent-Session-ID": currentSessionId
          }}
          renderToolCalls={[
            WebSeachToolCallRenderer,
            ThinkToolCallRenderer
          ]}
          key={currentSessionId}
          threadId={currentSessionId}
        >
          <Chat sessionId={currentSessionId} />
        </CopilotKit>
      </div>
    </div>
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
