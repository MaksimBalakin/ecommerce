FROM python:3.13

EXPOSE 8000

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Use gunicorn for production, or manage.py for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

