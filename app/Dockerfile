# Use an official Python runtime as a base image
FROM python

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
# This step is placed before copying the rest of the code to leverage Docker cache
# If requirements.txt doesn't change, this layer won't rebuild
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: prevents pip from storing downloaded packages, saving space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Inform Docker that the container will listen on port 5000 at runtime
EXPOSE 5000

# Set environment variables for the Flask application
ENV FLASK_APP=app.py
ENV FLASK_ENV=development 
# Set to 'production' for production deployments

# Command to run the Flask application when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]