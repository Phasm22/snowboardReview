# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /home/code/software/snowboardReview

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /home/code/software/snowboardReview

# Expose the port the app runs on
EXPOSE 8000

# Copy the entrypoint script
COPY entrypoint.sh /home/code/software/snowboardReview/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["bash", "/home/code/software/snowboardReview/entrypoint.sh"]

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
