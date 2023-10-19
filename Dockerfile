# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP api/challenge_app/app.py

# Create and set the working directory
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY api/challenge_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the container
COPY . /app

# Expose the port that Flask will run on
EXPOSE 5001

# Define the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
