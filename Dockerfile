# Dockerfile, Image, Container
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

EXPOSE 5000
# What to execute when the container is started
CMD [ "python", "./app.py"]