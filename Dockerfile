FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6 libpng16-16 fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV MPLBACKEND=Agg
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
COPY . .
RUN python scripts/generate_mock_data.py || true
EXPOSE 8000
CMD ["gunicorn","-w","2","-b","0.0.0.0:8000","app:app"]
