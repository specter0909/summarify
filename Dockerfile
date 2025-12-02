# Dockerfile for Summarify Streamlit app
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Avoid bytecode, buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && apt-get install -y build-essential curl git libsndfile1 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app
COPY . /app

# Expose port for Streamlit
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]