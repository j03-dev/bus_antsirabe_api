FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN pip install .

EXPOSE 8080

CMD ["python", "main.py"]
