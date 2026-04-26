FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/mock_agent.py .

EXPOSE 8000 8022

CMD ["python", "mock_agent.py"]
