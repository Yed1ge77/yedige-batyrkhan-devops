FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOST=0.0.0.0 PORT=8000 APP_ENV=production
COPY app/ ./app/
COPY config/ ./config/
RUN groupadd --system app && useradd --system --gid app --no-create-home app
USER app
EXPOSE 8000
CMD ["python3", "-m", "app.main"]
