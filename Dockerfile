# Pull base image
FROM python:3.11.5-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy the wait-for-it.sh script
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Migrate database
#RUN python manage.py migrate

# Create superuser
#RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '1234')" | python manage.py shell
# Make port 8000 available to the world
EXPOSE 8000

# Run the application
CMD ["gunicorn", "HoliFund.wsgi:application", "--bind", "0.0.0.0:8000"]
