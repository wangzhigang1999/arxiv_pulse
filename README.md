# arXiv Pulse

<div align="center">

![Logo](logo.png)

**智能 arXiv 论文摘要服务 - 为研究人员打造的论文监控与摘要工具**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 📖 简介

arXiv Pulse 是一个智能的 arXiv 论文监控与摘要服务，旨在帮助研究人员及时追踪最新研究成果。系统能够：

- 🔍 **自动抓取** arXiv 最新论文（支持多个学科类别）
- 🎯 **关键词监控** 实时追踪您关注的研究领域
- 🤖 **AI 摘要生成** 使用大语言模型生成中文摘要
- 📱 **钉钉通知** 及时推送匹配的论文到钉钉群
- 💾 **数据存储** 持久化存储论文信息，便于后续检索

## ✨ 主要功能

### 1. 定时爬取
- 支持多个 arXiv 类别同时抓取
- 可配置抓取间隔（默认 60 分钟）
- 自动去重，避免重复存储

### 2. 关键词监控
- 支持多关键词监控（逗号分隔）
- 匹配论文标题和摘要
- 自动生成中文摘要并发送通知

### 3. AI 摘要生成
- 基于大语言模型（支持 OpenAI 兼容 API）
- 生成高质量中文摘要
- 默认使用阿里云通义千问模型

### 4. 钉钉集成
- 支持钉钉机器人 webhook
- 格式化消息推送
- 包含论文标题、摘要、作者、链接等信息

## 🛠️ 技术栈

- **Web 框架**: FastAPI
- **数据库**: MySQL (SQLAlchemy ORM)
- **定时任务**: APScheduler
- **LLM**: OpenAI 兼容 API（支持通义千问、GPT 等）
- **日志**: Loguru
- **配置管理**: Pydantic Settings

## 📦 安装

### 前置要求

- Python 3.12+
- MySQL 5.7+ 或 MySQL 8.0+
- LLM API Key（如阿里云 DashScope、OpenAI 等）

### 使用 pip 安装

```bash
# 克隆仓库
git clone <repository-url>
cd arxiv_pulse

# 安装依赖
pip install -r requirements.txt

# 或者使用 uv（推荐）
uv pip install -r requirements.txt
```

### 使用 Docker 部署

```bash
# 构建镜像
docker build -t arxiv-pulse .

# 运行容器
docker run -d \
  --name arxiv-pulse \
  -p 8000:8000 \
  --env-file .env \
  arxiv-pulse
```

## ⚙️ 配置

创建 `.env` 文件，配置以下环境变量：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/arxiv_pulse

# 抓取配置
CRAWL_INTERVAL_MINUTES=60
ARXIV_CATEGORIES=cs.AI,cs.CV,cs.LG,cs.CL,cs.NE,cs.SE,cs.DC,cs.DS,cs.DB,cs.IR,cs.ET,cs.GL,cs.IT,cs.MA
ARXIV_PAGE_SIZE=100

# 关键词监控
KEYWORDS=agent,LLM,transformer
SUMMARY_INTERVAL_MINUTES=30

# LLM 配置（支持 OpenAI 兼容 API）
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen3-max

# 钉钉配置
DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=your_token
```

### 配置说明

- **DATABASE_URL**: MySQL 数据库连接字符串
- **CRAWL_INTERVAL_MINUTES**: arXiv 抓取间隔（分钟）
- **ARXIV_CATEGORIES**: 要监控的 arXiv 类别（逗号分隔）
- **KEYWORDS**: 监控的关键词（逗号分隔）
- **SUMMARY_INTERVAL_MINUTES**: 关键词匹配检查间隔（分钟）
- **LLM_API_KEY**: 大语言模型 API Key
- **LLM_BASE_URL**: LLM API 基础 URL
- **LLM_MODEL**: 使用的模型名称
- **DINGTALK_WEBHOOK_URL**: 钉钉机器人 webhook URL

## 🚀 使用方法

### 启动服务

```bash
# 直接运行
python -m arxiv_pulse.main

# 或使用命令行工具
arxiv-pulse

# 服务默认运行在 http://0.0.0.0:8000
```

### API 端点

- `GET /` - 根端点，返回 API 信息
- `GET /health` - 健康检查端点

访问 `http://localhost:8000/docs` 查看完整的 API 文档（Swagger UI）。

### 查看日志

服务使用 Loguru 进行日志记录，日志会输出到控制台。日志级别包括：
- INFO: 常规操作信息
- SUCCESS: 成功操作
- WARNING: 警告信息
- ERROR: 错误信息

## 📊 工作流程

1. **定时抓取**: 系统按配置的间隔从 arXiv 抓取最新论文
2. **数据存储**: 抓取的论文存储到 MySQL 数据库
3. **关键词匹配**: 定期检查新论文是否包含配置的关键词
4. **摘要生成**: 对匹配的论文使用 LLM 生成中文摘要
5. **通知推送**: 通过钉钉机器人发送论文通知

## 🗄️ 数据库

系统会自动创建以下表：

- `arxiv_papers`: 存储 arXiv 论文信息
  - `id`: 论文 ID（主键）
  - `title`: 论文标题
  - `summary`: 英文摘要
  - `chinese_summary`: 中文摘要（AI 生成）
  - `authors`: 作者列表
  - `published`: 发布时间
  - `updated`: 更新时间
  - `categories`: 分类
  - `link`: arXiv 链接
  - `created_at`: 创建时间

## 🔧 开发

### 代码格式化

项目使用 Ruff 进行代码格式化和 linting：

```bash
# 格式化代码
ruff format .

# 检查代码
ruff check .
```

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请通过 Issue 反馈。

---

<div align="center">

**Made with ❤️ for researchers**

</div>

