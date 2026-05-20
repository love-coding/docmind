from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from app.database import Base


class DocumentDB(Base):
    """上传的文档"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)


class QAHistoryDB(Base):
    """问答历史记录"""
    __tablename__ = "qa_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text, nullable=True)  # JSON 字符串
    created_at = Column(DateTime, default=datetime.now)
