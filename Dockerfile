FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . /app

# 运行前需要创建 .env 文件（参考 .env.example）
EXPOSE 8803

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8803"]
