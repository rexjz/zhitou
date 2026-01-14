import React, { useEffect, useRef, useState } from "react";
import { Button, Spin } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import { CopilotKit } from "@copilotkit/react-core";

import { WebSeachToolCallRenderer } from "@/components/ToolCall/web_search";
import { ThinkToolCallRenderer } from "@/components/ToolCall/think";
import "@copilotkit/react-ui/styles.css";
import { useAgent } from "@copilotkitnext/react";
// import { ActionExecutionMessage, ResultMessage, TextMessage } from "@copilotkit/runtime-client-gql";
import { useGetSessionMessages } from "@/sdk/agent/agent";
import SessionListView from "@/components/AgentChat/SessionListView";
import type { SessionData } from "@/sdk/models/sessionData";
import { useCopilotMessagesContext } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

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

  const handleNewSession = () => {
    const newSessionId = generateSessionId();
    setCurrentSessionId(newSessionId);
    // Update URL without page reload
    const url = new URL(window.location.href);
    url.searchParams.set("sessionId", newSessionId);
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
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center"
        }}>
          <span style={{ fontWeight: "bold", fontSize: "16px" }}>
            历史会话
          </span>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleNewSession}
            size="small"
          >
            新会话
          </Button>
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
          // key={currentSessionId}
        // threadId={currentSessionId}
        >
          <ChatProvider sessionId={currentSessionId} />
        </CopilotKit>
      </div>
    </div>
  );
};

// ChatProvider sits inside CopilotKit and creates the shared agent instance
const ChatProvider = ({ sessionId }: { sessionId: string }) => {
  const { agent } = useAgent({ agentId: 'default' });

  return <Chat sessionId={sessionId} agent={agent} />;
};

const Chat = ({ sessionId, agent }: { sessionId: string; agent: ReturnType<typeof useAgent>['agent'] }) => {
  const { data, isLoading: apiLoading } = useGetSessionMessages(sessionId)
  const hasLoadedHistory = useRef(false);
  const lastLoadedSessionId = useRef<string | null>(null);
  const loadingStartTime = useRef<number | null>(null);
  const [isMinLoadingTime, setIsMinLoadingTime] = useState(true);

  // Ensure minimum loading time of 3 seconds
  const isLoading = apiLoading || isMinLoadingTime;

  console.log("agent.messages: ", agent.messages)
  console.log("agent.isRunning: ", agent.isRunning)

  // Reset loaded flag and start loading timer when session changes
  useEffect(() => {
    if (lastLoadedSessionId.current !== sessionId) {
      hasLoadedHistory.current = false;
      lastLoadedSessionId.current = sessionId;
      loadingStartTime.current = Date.now();
      setIsMinLoadingTime(true);

      // Set minimum loading time of 3 seconds
      const timer = setTimeout(() => {
        setIsMinLoadingTime(false);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [sessionId]);

  useEffect(() => {
    if (!agent.isRunning && !isLoading && data && !hasLoadedHistory.current) {
      console.log("Loading history for session:", sessionId, data.data)
      agent.setMessages(data?.data as any)
      hasLoadedHistory.current = true;
    }
  }, [agent, agent.isRunning, isLoading, data, sessionId]);

  return (
    <div className="h-[calc(100vh-152px)] w-full rounded-lg" style={{ position: 'relative' }}>
      <CopilotChat
        className="h-full w-full rounded-lg"
        labels={{ initial: "", placeholder: "在这里输入" }}
        suggestions="auto"
        hideStopButton
      />
      {isLoading && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          pointerEvents: 'all'
        }}>
          <Spin size="large" />
        </div>
      )}
    </div>
  );
};

export default BasicChatPage;
