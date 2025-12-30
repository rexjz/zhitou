import React, { useMemo } from "react";
import "@copilotkit/react-ui/styles.css";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { HttpAgent } from "@ag-ui/client";
import { WebSeachToolCallRenderer } from "@/components/ToolCall/web_search";

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
        WebSeachToolCallRenderer
      ]}
      // renderToolCalls={}
    >
      <Chat />
    </CopilotKit>
  );
};

const Chat = () => {
  return (
    <div className="flex justify-center items-center h-full w-full">
      <div className="h-full w-full rounded-lg">
        <CopilotChat
          className="h-full rounded-2xl max-w-6xl mx-auto"
          labels={{ initial: "Hi, I'm an agent. Want to chat?" }}
          suggestions="auto"
        />
      </div>
    </div>
  );
};

export default BasicChatPage;
