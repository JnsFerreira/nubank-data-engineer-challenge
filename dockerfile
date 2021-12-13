# Base image
FROM python:3.9.7-buster

# Copy all files to root folder
COPY . ./root

# Defining root as workdir
WORKDIR /root

# Installing python additional Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Running tests
RUN pytest tests/

# Runs the application
CMD ["python3", "run.py"]