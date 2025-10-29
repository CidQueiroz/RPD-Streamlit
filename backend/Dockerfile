# Use an official Python runtime as a parent image
FROM python:3.9-slim as builder

# Set environment variables for Oracle Instant Client
ENV ORACLE_HOME=/opt/oracle/instantclient_19_28
ENV LD_LIBRARY_PATH=$ORACLE_HOME

# Download and unzip Oracle Instant Client
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://download.oracle.com/otn_software/linux/instantclient/1928000/instantclient-basic-linux.x64-19.28.0.0.0dbru.zip && \
    unzip instantclient-basic-linux.x64-19.28.0.0.0dbru.zip && \
    mkdir -p /opt/oracle && \
    mv instantclient_19_28 /opt/oracle/

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Create a non-root user
RUN useradd -ms /bin/bash user
USER user

# Copy Oracle Instant Client from builder
COPY --from=builder /opt/oracle/instantclient_19_28 /opt/oracle/instantclient_19_28

# Set environment variables for Oracle Instant Client
ENV ORACLE_HOME=/opt/oracle/instantclient_19_28
ENV LD_LIBRARY_PATH=$ORACLE_HOME

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]