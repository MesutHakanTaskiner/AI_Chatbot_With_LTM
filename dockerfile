FROM python:3.11-slim
# Create working directory

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code to the container
COPY . .

# If you're using .env for environment variables etc.:
# COPY .env.example .env
# Start the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]