FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt
FROM python:3.12-slim
RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
USER appuser
HEALTHCHECK CMD python healthcheck.py || exit 1
CMD ["python","-m","app.worker"]
