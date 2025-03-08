# Use an official Python runtime as the base image
FROM python:2

# Set the working directory in the container
WORKDIR /src/frontEnd

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose a port if your application needs it
EXPOSE 8000

# Define the command to run your application
CMD ["python", "Application.py"]
