FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ARG APP_FILE=app.py
COPY ${APP_FILE} app.py

CMD ["python", "app.py"]
