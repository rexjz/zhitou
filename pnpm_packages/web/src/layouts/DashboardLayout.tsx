import { Outlet, useNavigate, Link } from "react-router";
import ProLayout, { PageContainer } from '@ant-design/pro-layout';
import { ConfigProvider } from 'antd';
import { menuData } from '@/menuData';
import { useState } from "react";
// import 'antd/dist/reset.css';
// import '@ant-design/pro-layout/dist/layout.css';

export function DashboardLayout() {

  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState<boolean>(false)

  return (
    <ConfigProvider>
      <ProLayout
        title=""
        layout="side"
        navTheme="light"
        menuDataRender={() => menuData}
        menuItemRender={(item, dom) => (
          <Link to={item.path || '/dashboard'}>{dom}</Link>
        )}
        collapsed={collapsed}
        onCollapse={(b) => setCollapsed(b)}
      >
        <PageContainer>
          <Outlet />
        </PageContainer>
      </ProLayout>
    </ConfigProvider>
  );
}
