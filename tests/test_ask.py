"""
问答接口测试
"""


class TestAsk:
    """测试问答"""

    def test_ask_without_documents(self, client):
        """没有上传文档时提问，返回 400"""
        resp = client.post("/ask", json={"question": "几点关门"})
        assert resp.status_code == 400
        assert "请先上传文档" in resp.json()["detail"]

    def test_ask_after_upload(self, client):
        """上传文档后提问，返回答案和来源"""
        # 先上传文档
        client.post("/documents/upload",
                    files={"file": ("rules.txt", "营业时间：10点到22点", "text/plain")})
        # 提问
        resp = client.post("/ask", json={"question": "几点开门"})
        assert resp.status_code == 200
        data = resp.json()
        assert "answer" in data
        assert "sources" in data
        assert len(data["sources"]) > 0


class TestHistory:
    """测试问答历史"""

    def test_history_empty(self, client):
        """没有问答时返回空列表"""
        resp = client.get("/history")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_history_after_ask(self, client):
        """问答后历史记录不为空"""
        client.post("/documents/upload",
                    files={"file": ("rules.txt", "营业时间：10点到22点", "text/plain")})
        client.post("/ask", json={"question": "几点开门"})
        resp = client.get("/history")
        assert len(resp.json()) >= 1
        assert resp.json()[0]["question"] == "几点开门"
