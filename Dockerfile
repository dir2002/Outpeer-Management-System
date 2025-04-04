FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir && rm -f requirements.txt

RUN groupadd -g 1000 appgroup && useradd -r -u 1000 -g appgroup app

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && exec python manage.py runserver 0.0.0.0:8000"]