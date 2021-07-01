FROM python:3.6.6
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD nginx.conf /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
