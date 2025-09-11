FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (for caching layer)
COPY requirements.txt .

# Install dependencies (empty file = no error)
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run the app by default
CMD ["python", "app.py"]
