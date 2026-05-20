"""
Pydantic 模型：定义 API 请求和响应的数据格式
"""
from datetime import datetime

from pydantic import BaseModel


# ========== 文档相关 ==========

class DocumentResponse(BaseModel):
    id: int
    filename: str
    chunk_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentDetailResponse(DocumentResponse):
    """文档详情，包含全文内容"""
    content: str


# ========== 问答相关 ==========

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


class QAHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ========== 通用 ==========

class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    doc_count: int
    history_count: int
