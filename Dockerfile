FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Collect static files (optional, if you use staticfiles)
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "vikbo.wsgi:application", "--bind", "0.0.0.0:8000"]
