FROM python:3.12-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY src/ ./src

EXPOSE 5000

CMD ["gunicorn", "--threads", "2", "-b", "0.0.0.0:5000", "app:app"]

