"""
问答路由：提问、历史记录
"""
import json
import os

from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import QAHistoryDB
from app.schemas import AskRequest, AskResponse, QAHistoryResponse
from app.routers.documents import rag

router = APIRouter(tags=["问答"])

# DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


@router.post("/ask", response_model=AskResponse)
def ask_question(req: AskRequest, db: Session = Depends(get_db)):
    """基于已上传的文档回答问题"""
    # 检查是否有文档
    if rag.chunk_vectors is None or len(rag.chunks) == 0:
        raise HTTPException(status_code=400, detail="知识库为空，请先上传文档")

    # 1. RAG 搜索
    results = rag.search(req.question, top_k=3)
    if not results:
        raise HTTPException(status_code=404, detail="未找到相关内容")

    # 2. 拼接上下文
    context = "\n---\n".join([chunk for chunk, _ in results])
    sources = [chunk for chunk, _ in results]

    # 3. 调用 DeepSeek
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"基于以下文档内容回答问题：\n\n{context}"},
            {"role": "user", "content": req.question}
        ]
    )
    answer = resp.choices[0].message.content

    # 4. 保存问答历史
    history = QAHistoryDB(
        question=req.question,
        answer=answer,
        sources=json.dumps(sources, ensure_ascii=False)
    )
    db.add(history)
    db.commit()

    return AskResponse(answer=answer, sources=sources)


@router.get("/history", response_model=list[QAHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    """获取问答历史"""
    return db.query(QAHistoryDB).order_by(QAHistoryDB.id.desc()).all()
