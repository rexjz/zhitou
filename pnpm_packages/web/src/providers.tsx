import { useNavigate } from "react-router"
import { HelmetProvider } from "react-helmet-async"
export function Providers({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  return (
    <HelmetProvider>
      {children}
    </HelmetProvider>
  )
}