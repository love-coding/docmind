"""
AI 文档问答系统 - 应用入口
"""
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# 加载环境变量（必须在其他导入之前）
load_dotenv()

from app.database import engine, Base, get_db
from app.models import DocumentDB, QAHistoryDB
from app.routers import documents, ask

# 确保数据目录存在
Path("data").mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时创建表，关闭时清理"""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="DocMind - AI 文档问答系统",
    description="上传文档，基于 RAG 技术进行智能问答",
    version="1.0.0",
    lifespan=lifespan
)

# 注册路由
app.include_router(documents.router)
app.include_router(ask.router)


@app.get("/")
def root():
    return {
        "message": "DocMind API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """健康检查接口"""
    doc_count = db.query(DocumentDB).count()
    history_count = db.query(QAHistoryDB).count()
    return {
        "status": "ok",
        "doc_count": doc_count,
        "history_count": history_count
    }
