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

### 使用 uv 安装

```bash
# 克隆仓库
git clone <repository-url>
cd arxiv_pulse

# 安装依赖（包括开发依赖）
uv sync

# 或仅安装运行时依赖
uv sync --no-dev