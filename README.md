# 智投平台

## 仓库架构
基于uv workspace的monorepo架构
workspace members:
- **core:**
  核心类，存放数据repo层，公共类型，部分通用逻辑。其他的member应该都依赖core。
- **database:** 包含关系型数据库，包含数据库 orm entity 和 数据库migration和。
- **api:** 面向前端提供restful api的后端服务，主要包含所有的handler和一些需要小范围复用的service。
- **worker:** 独立启动的worker进程，主要用于定时任务（数据拉取和数据同步）

## 技术选型
- **关系型数据库：**PostgreSQL
- **RAG：**[RAGFLOW](https://github.com/infiniflow/ragflow)