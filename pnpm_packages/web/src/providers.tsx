import { useNavigate } from "react-router"
import { HelmetProvider } from "react-helmet-async"
import { SWRConfig } from "swr";

export function Providers({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  return (
    <HelmetProvider>
      <SWRConfig
        value={{
          onError: (error) => {
            if (error.response?.status === 401) {
              console.log("已登出");
            }
          },
        }}
      >
        {children}
      </SWRConfig>
    </HelmetProvider>
  )
}