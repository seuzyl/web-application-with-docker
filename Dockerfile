FROM public-docker-virtual.artnj.zte.com.cn/python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app
RUN pip install -i http://mirrors.zte.com.cn/pypi/simple --trusted-host mirrors.zte.com.cn -r requirements.txt