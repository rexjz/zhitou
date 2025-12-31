import React, { useMemo } from "react";
import "@copilotkit/react-ui/styles.css";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { HttpAgent } from "@ag-ui/client";
import { WebSeachToolCallRenderer } from "@/components/ToolCall/web_search";
import { ThinkToolCallRenderer } from "@/components/ToolCall/think";

const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
};

const BasicChatPage: React.FC = () => {
  const sessionId = useMemo(() => {
    const params = new URLSearchParams(window.location.search);
    const sessionFromUrl = params.get("sessionId");
    return sessionFromUrl || generateSessionId();
  }, []);

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
      useSingleEndpoint
      // renderToolCalls={}
    >
      <Chat />
    </CopilotKit>
  );
};

const Chat = () => {
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
