FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=core.settings
ENV PORT=8000

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 300
