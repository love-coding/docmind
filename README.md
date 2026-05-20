# DocMind - AI 智能文档问答系统

上传文档，基于 RAG 技术进行智能问答。

## 技术栈

- **FastAPI** — Web 框架
- **SQLite + SQLAlchemy** — 数据库
- **NumPy** — 词频向量 + 余弦相似度（RAG 检索）
- **DeepSeek API** — AI 回答生成
- **pytest** — 单元测试
- **Docker** — 容器化部署

## 功能

| 功能 | 说明 |
|------|------|
| 文档管理 | 上传 .txt 文档、列表、详情、删除 |
| 智能问答 | 基于文档内容提问，AI 回答并标注来源 |
| 问答历史 | 自动保存每次问答记录 |

## 快速开始

### 本地运行

```bash
# 1. 创建 .env 文件（参考 .env.example）
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
uvicorn app.main:app --port 8803

# 4. 打开浏览器访问
# http://localhost:8803/docs
```

### Docker 运行

```bash
# 1. 构建镜像
docker build -t docmind .

# 2. 运行容器（需要挂载 .env）
docker run -p 8803:8803 \
  -v $(pwd)/.env:/app/.env \
  docmind
```

### 运行测试

```bash
pytest tests/ -v
```

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/documents/upload` | 上传 .txt 文档 |
| GET | `/documents` | 文档列表 |
| GET | `/documents/{id}` | 文档详情 |
| DELETE | `/documents/{id}` | 删除文档 |
| POST | `/ask` | 提问 |
| GET | `/history` | 问答历史 |
| GET | `/health` | 健康检查 |

## 项目结构

```
docmind/
├── app/
│   ├── main.py               # 入口
│   ├── database.py            # 数据库配置
│   ├── models.py              # ORM 模型
│   ├── schemas.py             # Pydantic 模型
│   ├── knowledge_base.py      # 词表 + 向量化
│   ├── routers/
│   │   ├── documents.py       # 文档 CRUD
│   │   └── ask.py             # 问答接口
│   └── services/
│       └── rag.py             # RAG 检索服务
├── tests/
│   ├── conftest.py            # 测试配置
│   ├── test_documents.py      # 文档测试
│   └── test_ask.py            # 问答测试
├── Dockerfile
├── requirements.txt
└── README.md
```

## 工作原理

```
用户上传 .txt → 切片 → 向量化 → 存入索引
用户提问     → 向量化 → 余弦相似度搜索 → 找到最相关片段
             → 拼入 prompt → 调 DeepSeek API → 返回答案 + 来源
```
