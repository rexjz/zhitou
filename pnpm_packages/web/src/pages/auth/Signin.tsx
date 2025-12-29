import {
  LockOutlined,
  UserOutlined,
} from '@ant-design/icons';
import {
  LoginForm,
  ProConfigProvider,
  ProFormText,
} from '@ant-design/pro-components';
import { message, theme } from 'antd';
import { useNavigate } from 'react-router';
import { useSigninUpass } from '@/sdk/auth/auth';
import type { SignInRequest } from '@/sdk/models';

function SignInPage() {
  const { token } = theme.useToken();
  const { trigger, isMutating } = useSigninUpass();
  const navigate = useNavigate();

  const handleSubmit = async (values: SignInRequest) => {
    try {
      await trigger(values);
      message.success('登录成功！');
      navigate('/dashboard');
    } catch (error) {
      message.error('登录失败，请检查用户名和密码');
    }
  };

  return (
    <ProConfigProvider hashed={false}>
      <div style={{
        backgroundColor: token.colorBgContainer,
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <LoginForm
          title="欢迎"
          subTitle="请输入您的账号和密码"
          onFinish={handleSubmit}
          loading={isMutating}
        >
          <ProFormText
            name="username"
            fieldProps={{
              size: 'large',
              prefix: <UserOutlined className={'prefixIcon'} />,
            }}
            placeholder={'请输入用户名'}
            rules={[
              {
                required: true,
                message: '请输入用户名!',
              },
            ]}
          />
          <ProFormText.Password
            name="password"
            fieldProps={{
              size: 'large',
              prefix: <LockOutlined className={'prefixIcon'} />,
            }}
            placeholder={'请输入密码'}
            rules={[
              {
                required: true,
                message: '请输入密码！',
              },
            ]}
          />
        </LoginForm>
      </div>
    </ProConfigProvider>
  );
}

export default SignInPage;