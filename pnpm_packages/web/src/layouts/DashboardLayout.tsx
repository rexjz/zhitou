import { Outlet, useNavigate, Link } from "react-router";
import ProLayout, { PageContainer } from '@ant-design/pro-layout';
import { ConfigProvider, Dropdown, message } from 'antd';
import { LogoutOutlined, UserOutlined } from '@ant-design/icons';
import { menuData } from '@/menuData';
import { useState } from "react";
import { useGetCurrentUser } from "@/sdk/user/user"
import { useSignout } from "@/sdk/auth/auth"


export function DashboardLayout() {

  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState<boolean>(false)
  const { data: currentUserData } = useGetCurrentUser();
  const { trigger: signout, isMutating: isSigningOut } = useSignout();

  const currentUser = currentUserData?.data?.data;

  const handleSignout = async () => {
    try {
      await signout({});
      navigate('/signin');
    } catch (error) {
    }
  };

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
        avatarProps={{
          src: undefined,
          size: 'small',
          title: currentUser?.username || '用户',
          icon: <UserOutlined />,
          render: (props, dom) => {
            return (
              <Dropdown
                menu={{
                  items: [
                    {
                      key: 'userInfo',
                      icon: <UserOutlined />,
                      label: currentUser?.email || '未知邮箱',
                      disabled: true,
                    },
                    {
                      type: 'divider',
                    },
                    {
                      key: 'signout',
                      icon: <LogoutOutlined />,
                      label: '退出登录',
                      onClick: handleSignout,
                      disabled: isSigningOut,
                    },
                  ],
                }}
              >
                {dom}
              </Dropdown>
            );
          },
        }}
      >
        <PageContainer>
          <Outlet />
        </PageContainer>
      </ProLayout>
    </ConfigProvider>
  );
}
