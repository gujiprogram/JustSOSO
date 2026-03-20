# 使用官方 Python 镜像作为基础镜像
FROM python:3.10

# 将工作目录设置为 /app
WORKDIR /app

# 将 requirements.txt 复制到容器的 /app 目录中
COPY requirements.txt /app

# 安装依赖
RUN pip install -r requirements.txt

# 将当前目录中的文件复制到容器的 /app 目录中
COPY . /app

# 开放容器的 5000 端口
EXPOSE 5000

# 在容器启动时运行 main.py
CMD ["python", "main.py"]
