import React, { useEffect, useMemo } from "react";

import { CopilotKit } from "@copilotkit/react-core";

import { WebSeachToolCallRenderer } from "@/components/ToolCall/web_search";
import { ThinkToolCallRenderer } from "@/components/ToolCall/think";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { useAgent } from "@copilotkitnext/react";
// import { ActionExecutionMessage, ResultMessage, TextMessage } from "@copilotkit/runtime-client-gql";

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
      key={sessionId}
      threadId={sessionId}
    >
      <Chat />
    </CopilotKit>
  );
};

const Chat = () => {
  // const { messages, setMessages } = useCopilotMessagesContext()
  // console.log(messages)
  // useEffect(() => {
  //   if (messages.length !== 0) {
  //     localStorage.setItem("copilotkit-messages", JSON.stringify(messages));
  //   }
  // }, [JSON.stringify(messages)]);

  const { agent } = useAgent({agentId: "default"});  
  const { state, setState, messages } = agent;
  console.log(messages)
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
