# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the Oracle Wallet and set TNS_ADMIN
COPY Wallet_CDKTECKDB /opt/oracle/wallet
ENV TNS_ADMIN=/opt/oracle/wallet

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
# The command should be something like:
# gunicorn core.wsgi:application --bind 0.0.0.0:8000
# We will set the final command during the OCI deployment phase
# For now, this is a good starting point.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
