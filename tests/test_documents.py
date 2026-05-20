"""
文档管理接口测试
"""
import io


class TestDocumentUpload:
    """测试文档上传"""

    def test_upload_txt(self, client):
        """上传 .txt 文件，验证返回文档信息"""
        resp = client.post(
            "/documents/upload",
            files={"file": ("test.txt", "门店营业时间：每天10点开门", "text/plain")}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["filename"] == "test.txt"
        assert data["id"] == 1

    def test_upload_empty_file(self, client):
        """上传空文件，返回 400"""
        resp = client.post(
            "/documents/upload",
            files={"file": ("empty.txt", "", "text/plain")}
        )
        assert resp.status_code == 400

    def test_upload_multiple(self, client):
        """上传多个文档，验证列表长度"""
        for i in range(3):
            client.post(
                "/documents/upload",
                files={"file": (f"doc{i}.txt", f"文档{i}内容", "text/plain")}
            )
        resp = client.get("/documents")
        assert len(resp.json()) == 3


class TestDocumentList:
    """测试文档列表"""

    def test_list_empty(self, client):
        """没有文档时返回空列表"""
        resp = client.get("/documents")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_after_upload(self, client):
        """上传后列表不为空"""
        client.post("/documents/upload",
                    files={"file": ("doc.txt", "测试内容", "text/plain")})
        resp = client.get("/documents")
        assert len(resp.json()) == 1


class TestDocumentDetail:
    """测试文档详情"""

    def test_get_detail(self, client):
        """获取文档详情，验证包含内容字段"""
        client.post("/documents/upload",
                    files={"file": ("doc.txt", "测试内容", "text/plain")})
        resp = client.get("/documents/1")
        assert resp.status_code == 200
        assert resp.json()["content"] == "测试内容"

    def test_get_not_found(self, client):
        """不存在的文档返回 404"""
        resp = client.get("/documents/999")
        assert resp.status_code == 404


class TestDocumentDelete:
    """测试文档删除"""

    def test_delete(self, client):
        """删除文档后列表为空"""
        client.post("/documents/upload",
                    files={"file": ("doc.txt", "测试内容", "text/plain")})
        resp = client.delete("/documents/1")
        assert resp.status_code == 200
        assert resp.json()["message"] == "文档已删除"
        # 验证列表为空
        resp = client.get("/documents")
        assert resp.json() == []

    def test_delete_not_found(self, client):
        """删除不存在的文档返回 404"""
        resp = client.delete("/documents/999")
        assert resp.status_code == 404
