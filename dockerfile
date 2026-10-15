FROM python:3.12-slim

WORKDIR /project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN useradd -m appuser && \
    chown -R appuser:appuser /project

USER appuser

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app/app.py"]