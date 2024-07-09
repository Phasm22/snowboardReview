# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files
COPY . /code/

# Expose the port the app runs on
EXPOSE 8050

# Copy the entrypoint script
COPY entrypoint.sh /code/entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]
# Set the entrypoint

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8050"]
