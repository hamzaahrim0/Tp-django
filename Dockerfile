# 1. Base: a minimal Linux that already has Python 3.12
FROM python:3.12-slim

# 2. Python behaves better in containers with these two
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Working folder inside the image
WORKDIR /app

# 4. Dependencies FIRST, in their own layer (cache!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now the code (changes often, so it comes after)
COPY . .

# 6. Bake the model into the image (same sklearn version as serving)
RUN python -c "from dashboard.ml import train; print('accuracy', train())"

# 7. Collect static files at build time
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput

# 8. Non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# 9. Document the port + start command
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
