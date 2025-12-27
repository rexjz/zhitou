import { BrowserRouter } from "react-router";
import { Routes, Route, Navigate } from "react-router";
import { Providers } from "./providers";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { Helmet } from "react-helmet-async";
import HomePage from "./pages/HomePage";
import Page2 from "./pages/Page2";


const App = () => {
  return (
    <BrowserRouter>
      <Providers>
        <Helmet>
          <title>react-webpack-tailwindcss-template</title>
        </Helmet>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardLayout />}>
            <Route index element={<HomePage />} />
            <Route path="page2" element={<Page2 />} />
          </Route>
        </Routes>
      </Providers>
    </BrowserRouter>
  );
};



export default App;