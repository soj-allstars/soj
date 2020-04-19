FROM python:3.8-alpine
WORKDIR /usr/src/soj

COPY requirements.txt ./
RUN apk update && apk add --update --no-cache mariadb-connector-c-dev && \
	apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		musl-dev \
		libffi-dev \
		make && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir --upgrade pip && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt && \
    apk del .build-deps

COPY . .

ENTRYPOINT ["uvicorn"]
CMD ["--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "soj.asgi:application"]
