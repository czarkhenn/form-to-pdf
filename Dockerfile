FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd -r django && useradd -r -g django django

# Install system dependencies for WeasyPrint
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fontconfig \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/cache/fontconfig /root/.cache/fontconfig \
    && fc-cache -f
# Set work directory
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media && \
    mkdir -p /home/django/.cache/fontconfig && \
    chown -R django:django /app /home/django/.cache

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

USER django

# Expose port
EXPOSE 8000

# Run the application
ENTRYPOINT ["/app/entrypoint.sh"]

