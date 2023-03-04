FROM python:3.8.16
EXPOSE 8000
RUN sed -i "s@http://deb.debian.org@http://mirrors.cloud.tencent.com@g" /etc/apt/sources.list && rm -Rf /var/lib/apt/lists/* && apt update && apt install -y libgl1
RUN pip install paddlepaddle paddleocr tencentcloud-sdk-python fastapi pydantic opencv-python scipy -i https://mirrors.cloud.tencent.com/pypi/simple
WORKDIR /src
COPY ./ocrapi ./ocrapi
COPY ./app.py ./
CMD [ "python", "app.py"]