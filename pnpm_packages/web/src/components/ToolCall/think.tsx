import { ReactToolCallRenderer } from "@copilotkitnext/react";
import { z } from "zod";

const think_args_schema = z.object({
  title: z.string(),
  confidence: z.number(),
  thought: z.string(),
  action: z.string()
})

export const ThinkToolCallRenderer: ReactToolCallRenderer<z.infer<typeof think_args_schema>> = {
  name: "think",
  args: think_args_schema,
  render: (props) => {
    switch (props.status) {
      case "inProgress":
      case "executing":
        return (
          <div className="animate-pulse">
            🤔 正在思考…
          </div>
        );

      case "complete":
        const result = props.result;
        return (
          <div className="my-2">
            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1 font-medium">
              💭 思考过程
            </div>
            <blockquote className="border-l-4 border-gray-300 dark:border-gray-600 pl-4 py-2 italic text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800/50 rounded-r">
              {result}
            </blockquote>
          </div>
        );
    }
  }
}
