import { CopilotChat } from "@copilotkit/react-ui";
import { ReactToolCallRenderer, } from "@copilotkitnext/react"
import { z } from "zod";

const web_search_args_schema = z.object({
  query: z.string(),
  count: z.number()
})

export const WebSeachToolCallRenderer: ReactToolCallRenderer<z.infer<typeof web_search_args_schema>> = {
  name: "web_search",
  args: web_search_args_schema,
  render: (props) => {
    switch (props.status) {
      case "inProgress":
        return (
          <div className="text-gray-400">
            🤔 正在理解搜索条件…
          </div>
        );

      case "executing":
        return (
          <div className="animate-pulse">
            🔍 正在搜索：<b>{props.args.query}</b>
          </div>
        );

      case "complete":
        return (
          <div>
            ✅ 网络搜索：
            <pre>{props.result}</pre>
          </div>
        );
    }
  }
}