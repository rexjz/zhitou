# 智投平台

## 仓库架构
基于uv workspace的monorepo架构
workspace members:
- **core:** 核心类，存放数据repo层，公共类型，部分通用逻辑。其他的member应该都依赖core。在设计任何功能时，core包不应当再依
  项目中其他任何member，以避免循环依赖。
- **database:** 包含关系型数据库，包含数据库 orm entity 和 数据库migration和。
- **api:** 面向前端提供restful api的后端服务，主要包含所有的handler和一些需要小范围复用的service。
- **worker:** 独立启动的worker进程，主要用于定时任务（数据拉取和数据同步，定时触发一些算法更新预测值等）
- **zhitou_agent:** LLM agent package。LLM 投资顾问智能体。
- **zhitou_ml:** machine learning package。目前主要包含一个企业财务造假风险预测算法。

## 技术选型
- **关系型数据库：**PostgreSQL
- **RAG：**[RAGFLOW](https://github.com/infiniflow/ragflow)
  
## Code Formatting
python 文件使用 ruff 作为 formatter，formatter 配置在 ruff.toml 中。开发时请在IDE中配置ruff插件为python文件的formatter，一般都会自动读取项目根目录下的 ruff.toml 配置。


## 常用命令
> 所有命令在项目根目录运行

### 启动服务

#### api
```
uv run --package api api
```

#### worker
```
uv run --package worker annual_report_worker
```

### 数据库migration
```bash
# 查看当前指针
uv run --package database_migration alembic -c packages/database_migration/src/database_migration/alembic.ini current

# migration version自动生成
uv run --package database_migration alembic -c packages/database_migration/src/database_migration/alembic.ini revision --autogenerate -m "<describe the change>"

# apply最新version
uv run --package database_migration alembic -c packages/database_migration/src/database_migration/alembic.ini upgrade head
```