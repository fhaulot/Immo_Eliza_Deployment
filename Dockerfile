# Use Ubuntu as base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.10 and other necessary tools
RUN apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN python3.10 -m pip install --upgrade pip

# Create working directory
RUN mkdir /app
WORKDIR /app

# Copy your project files to /app
COPY . /app

# Install Python dependencies from requirements.txt if exists,
# otherwise install manually (adjust as needed)
# If you don't have requirements.txt, list your dependencies here
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Expose port (default FastAPI port)
EXPOSE 8000

# Command to run the app
CMD ["python3.10", "app.py"]
