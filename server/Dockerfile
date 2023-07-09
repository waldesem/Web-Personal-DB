# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY app app

# Set the entry point command using flask run
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Set the entry point command using gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]