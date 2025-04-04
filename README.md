# MCP 计算网关 ⚡

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![架构: 微服务](https://img.shields.io/badge/architecture-microservices-green.svg)]()
[![测试: Pytest](https://img.shields.io/badge/testing-pytest-00C4CC.svg)]()

分布式计算网关系统，提供统一的MCP协议接入层和原子计算能力抽象。
## ✨ 核心功能

- 🧮 四则运算工具集（加减乘除）
- 📡 基于SSE的实时消息传输
- ⚡ 异步HTTP客户端支持
- 🔒 强类型输入校验
- 📊 支持多内容类型返回（文本/图片/嵌入式资源）

## 🛠️ 技术栈

- 框架: [Starlette](https://www.starlette.io/)
- 服务器: [Uvicorn](https://www.uvicorn.org/)
- HTTP客户端: [HTTPX](https://www.python-httpx.org/)
- 协议: [MCP Server-Sent Events](mcp-server-sse-docs)

## 🚀 快速开始

### 前置要求
- Python 3.10+
- Pipenv

```bash
# 安装依赖
pip install -r requirements.txt

## 🌟 系统架构
```mermaid
graph LR
    Client-->|SSE Streaming| MCP_Server["MCP Server (Port 8001)"]
    MCP_Server-->|HTTP RPC| API_Server["API Server (Port 8000)"]
    API_Server-.->|计算原子| DB[(内存存储)]
    
    subgraph 计算集群
        API_Server
    end
