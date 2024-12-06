# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the rest of the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the application
EXPOSE 7860

# Ensure Gradio listens on all network interfaces
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]
