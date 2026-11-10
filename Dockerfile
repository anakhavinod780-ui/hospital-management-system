
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run database migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn HMS.wsgi:application --bind 0.0.0.0:$PORT"]
