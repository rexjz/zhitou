import { CopilotChat } from "@copilotkit/react-ui";
import { ReactToolCallRenderer, } from "@copilotkitnext/react"
import { z } from "zod";

const web_search_args_schema = z.object({
  query: z.string(),
  count: z.number()
})

const web_search_result_schema = z.object({
  query: z.string(),
  webResults: z.array(z.object({
    name: z.string(),
    url: z.string(),
    snippet: z.string(),
    siteName: z.string().optional(),
    dateLastCrawled: z.string().optional()
  }))
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
        try {
          console.log(typeof props.result)
          const result = typeof props.result === 'string'
            ? JSON.parse(props.result)
            : props.result;

          const parsedResult = web_search_result_schema.safeParse(result);

          if (!parsedResult.success) {
            return (
              <div className="text-red-500">
                ❌ 解析搜索结果失败
                <pre className="text-xs mt-2">{props.result}</pre>
              </div>
            );
          }

          const { query, webResults } = parsedResult.data;

          return (
            <div className="space-y-3">
              <div className="text-sm text-gray-600 dark:text-gray-400">
                ✅ 找到 <b>{webResults.length}</b> 条关于「<b>{query}</b>」的结果
              </div>

              <div className="space-y-2">
                {webResults.map((result, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-3 hover:border-blue-400 dark:hover:border-blue-600 transition-colors"
                  >
                    <a
                      href={result.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block group"
                    >
                      <h3 className="text-blue-600 dark:text-blue-400 font-medium text-sm group-hover:underline line-clamp-2">
                        {result.name}
                      </h3>

                      <div className="flex items-center gap-2 mt-1 text-xs text-gray-500 dark:text-gray-400">
                        {result.siteName && (
                          <span className="font-medium">{result.siteName}</span>
                        )}
                        {result.dateLastCrawled && (
                          <>
                            <span>•</span>
                            <span>{new Date(result.dateLastCrawled).toLocaleDateString('zh-CN')}</span>
                          </>
                        )}
                      </div>

                      <p className="text-sm text-gray-700 dark:text-gray-300 mt-2 line-clamp-3">
                        {result.snippet}
                      </p>

                      <div className="text-xs text-gray-400 dark:text-gray-500 mt-2 truncate">
                        {result.url}
                      </div>
                    </a>
                  </div>
                ))}
              </div>
            </div>
          );
        } catch (error) {
          console.log(error)
          return (
            <div className="text-red-500">
              ❌ 渲染搜索结果时出错
              <pre className="text-xs mt-2">{props.result}</pre>
            </div>
          );
        }
    }
  }
}