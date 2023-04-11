FROM python:3.11-slim

RUN pip install --upgrade pip &&\
	pip install boto3 python-dotenv &&\
	rm -f /var/lib/apt/lists/*

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["/entrypoint.py"]
