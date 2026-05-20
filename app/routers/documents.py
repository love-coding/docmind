"""
文档管理路由：上传、列表、详情、删除
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DocumentDB
from app.schemas import DocumentResponse, DocumentDetailResponse
from app.services.rag import RAGService

# 全局 RAG 服务实例
rag = RAGService()

router = APIRouter(prefix="/documents", tags=["文档管理"])


def rebuild_rag_index(db: Session) -> None:
    """从数据库加载所有文档，重新建 RAG 索引"""
    docs = db.query(DocumentDB).all()
    documents = [(doc.id, doc.content) for doc in docs]
    rag.rebuild(documents)


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传 .txt 文档"""
    content = await file.read()
    text = content.decode("utf-8")
    if not text.strip():
        raise HTTPException(status_code=400, detail="文件内容不能为空")

    doc = DocumentDB(filename=file.filename, content=text)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    rebuild_rag_index(db)
    return doc


@router.get("", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    """获取文档列表"""
    return db.query(DocumentDB).order_by(DocumentDB.id.desc()).all()


@router.get("/{doc_id}", response_model=DocumentDetailResponse)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    """获取文档详情"""
    doc = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    return doc


@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """删除文档"""
    doc = db.query(DocumentDB).filter(DocumentDB.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")

    db.delete(doc)
    db.commit()
    rebuild_rag_index(db)
    return {"message": "文档已删除"}
