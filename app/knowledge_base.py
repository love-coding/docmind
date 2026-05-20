"""
知识库核心：词表构建 + 向量化

功能：
1. 接收文档列表，提取所有不重复的字作为词表
2. 把文本转成词频向量（用于后续 RAG 搜索）
"""
import re
from collections import Counter


class KnowledgeBase:
    """
    管理词表和向量化。

    用法：
        kb = KnowledgeBase()
        kb.build(["文档1内容", "文档2内容"])
        vector = kb.embed("用户问题")
    """

    def __init__(self):
        self.word_list: list[str] = []

    # ============================================================
    # TODO: 写 tokenize 方法
    # 输入文本，返回单字/单词列表
    # 提示：re.findall(r"[a-zA-Z0-9]+|[一-鿿]", text)
    # ============================================================
    def _tokenize(self, text: str) -> list[str]:
        # TODO: 写代码
        return re.findall(r'[a-zA-Z0-9]+|[一-鿿]',text)

    # ============================================================
    # TODO: 写 build 方法
    # 输入文档列表，建立词表（排序、去重）
    # 提示：self.word_list = sorted(set(...))
    # ============================================================
    def build(self, texts: list[str]) -> None:
        # TODO: 写代码
        self.word_list = sorted(set(w for d in texts for w in self._tokenize(d)))

    # ============================================================
    # TODO: 写 embed 方法
    # 输入文本，返回词频向量（列表，每个元素是 float）
    # 提示：Counter + 遍历 word_list 取值
    # ============================================================
    def embed(self, text: str) -> list[float]:
        # TODO: 写代码
        tokens = self._tokenize(text)
        cnt = Counter(tokens)
        return [float(cnt.get(w, 0)) for w in self.word_list]
