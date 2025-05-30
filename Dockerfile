FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install fastapi uvicorn httpx openai==0.28
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]