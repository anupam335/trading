FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

# Default environment variables (can be overridden)
ENV VEDA_TICKER="^NSEI"
ENV VEDA_MINUTES=60

CMD ["python", "-m", "python.main", "schedule", "^NSEI", "--minutes", "60"]
