"""
RAG 检索服务：切分文档、建立索引、相似搜索
"""
import json

import numpy as np

from app.knowledge_base import KnowledgeBase


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 30) -> list[str]:
    """
    将长文本切成小块，块之间有重叠。

    参数：
        text: 原始文本
        chunk_size: 每块字符数
        overlap: 相邻块重叠字符数

    返回：
        字符串列表，每块是文本片段
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


class RAGService:
    """
    管理文档索引和相似搜索。

    工作流程：
        1. add_document(text) → 切片 → 向量化 → 加入索引
        2. search(query, top_k) → 向量化 → 余弦相似度 → 返回最匹配的块
    """

    def __init__(self):
        self.kb = KnowledgeBase()
        # 索引数据
        self.chunks: list[str] = []           # 所有文本块
        self.chunk_vectors: np.ndarray | None = None  # 所有块向量
        self.chunk_doc_map: list[int] = []    # 每个块对应的文档ID

    # ============================================================
    # TODO: 写 rebuild 方法
    # 输入文档列表 [(doc_id, content), ...]，重建整个索引
    #
    # 步骤：
    # 1. 清空 self.chunks、self.chunk_doc_map
    # 2. 遍历所有文档，对每个文档调用 chunk_text
    # 3. 把切出的块加入 self.chunks，对应的 doc_id 加入 self.chunk_doc_map
    # 4. 用 self.kb.build() 从 chunks 建词表
    # 5. 用 np.array 把所有块转成向量矩阵 self.chunk_vectors
    #
    # 提示：
    # - 类型：documents 是 list[tuple[int, str]]，如 [(1, "文档内容"), ...]
    # - 向量化：self.kb.embed(chunk) 返回 list[float]
    # - chunk_vectors 的 dtype 设为 float
    # ============================================================
    def rebuild(self, documents: list[tuple[int, str]]) -> None:
        # 清空旧数据
        self.chunks = []
        self.chunk_doc_map = []

        # 遍历所有文档，切片
        for doc_id, content in documents:
            doc_chunks = chunk_text(content)
            self.chunks.extend(doc_chunks)
            self.chunk_doc_map.extend([doc_id] * len(doc_chunks))

        # 用所有 chunks 建词表
        self.kb.build(self.chunks)

        # 所有块转成向量矩阵
        vectors = [self.kb.embed(chunk) for chunk in self.chunks]
        self.chunk_vectors = np.array(vectors, dtype=float)


    # ============================================================
    # TODO: 写 search 方法
    # 输入 query（字符串）和 top_k，返回最匹配的文本块列表
    #
    # 步骤：
    # 1. 用 self.kb.embed(query) 转成向量 q_vec
    # 2. 用 np.array 把 q_vec 包一下，dtype=float
    # 3. 计算余弦相似度：
    #    sim = np.dot(q_vec, chunk_vector) / (norm(q_vec) * norm(chunk_vector) + 1e-10)
    # 4. 按相似度排序，取前 top_k
    # 5. 返回 [(文本块, 相似度), ...]
    #
    # 提示：
    # - 用 enumerate 遍历 self.chunk_vectors
    # - 用 np.linalg.norm 算长度
    # - 用 sorted(..., key=lambda x: x[1], reverse=True) 排序
    # ============================================================
    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        """搜索最相关的文档块"""
        q_vec = np.array(self.kb.embed(query), dtype=float)
        q_norm = np.linalg.norm(q_vec)

        # 遍历所有块向量，算余弦相似度
        scores = []
        for i, doc_vec in enumerate(self.chunk_vectors):
            sim = np.dot(q_vec, doc_vec) / (q_norm * np.linalg.norm(doc_vec) + 1e-10)
            scores.append((i, sim))

        # 按相似度降序排序，取前 top_k
        scores.sort(key=lambda x: x[1], reverse=True)
        return [(self.chunks[idx], float(score)) for idx, score in scores[:top_k]]
