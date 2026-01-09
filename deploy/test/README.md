# Test 环境部署说明

数据库，和Redis采用云服务
数据库和Redis的连接地址受 ./config 下对应环境的配置文件控制

RagFlow使用单独的 composefile 启动，不包含在部署 composefile 中
Ragflow 的 es search 组件采用云服务，Ragflow 的 es search 地址受 .env 文件中的变量控制

