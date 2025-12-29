import { Navigate } from 'react-router';
import type { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

function getCookie(name: string) {
  const reg = new RegExp("(^|; )" + name + "=([^;]*)");
  const result = reg.exec(document.cookie);
  return result ? decodeURIComponent(result[2]) : null;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const accessToken = getCookie('zhitou-logged-in');
  console.log("accessToken", accessToken)
  if (!accessToken) {
    return <Navigate to="/signin" replace />;
  }

  return <>{children}</>;
}
