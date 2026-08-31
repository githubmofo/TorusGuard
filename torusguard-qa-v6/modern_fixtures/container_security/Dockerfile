FROM python:3.12-slim
WORKDIR /app
COPY . .
# Running as root user & hardcoding secrets
ENV DATABASE_PASSWORD="secret_in_docker"
CMD ["python", "main.py"]
