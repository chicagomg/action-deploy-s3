# Container image that runs your code
FROM python:3.11-slim

RUN pip install --upgrade pip &&\
	pip install boto3 python-dotenv &&\
	rm -f /var/lib/apt/lists/*

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.py /entrypoint.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
#ENTRYPOINT ["/entrypoint.py"]