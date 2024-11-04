FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/opt/repo \
    HOST=0.0.0.0 \
    PORT=80

# Set working directory
WORKDIR ${HOME}

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY Pipfile Pipfile.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv requirements --categories packages > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y pipenv && \
    rm -rf ~/.cache

# Copy the rest of the application code
COPY . .

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]