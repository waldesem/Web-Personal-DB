# Use the official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY /backend/requirements.txt .

# copy every content from the local file to the image
COPY /backend /app

# Install dependencies
RUN pip install -r requirements.txt

# Set the entry point command using gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]