FROM python:3.10.7

WORKDIR /app

COPY pyQQMail/ /app

# 配置国内镜像
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

#更新pip
RUN pip install --upgrade pip


RUN pip install -r requirements.txt

CMD ["python", "detectMessages.py"]

CMD ["python", "sendTiming.py"]