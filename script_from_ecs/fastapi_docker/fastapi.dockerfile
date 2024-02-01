FROM python:3.9

WORKDIR /app

COPY config.py /app/
COPY .env /app/
COPY fastapi.dockerfile /app/
COPY function /app/function/
COPY __init__.py /app/
COPY requirements.txt /app/
COPY main.py /app/

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
