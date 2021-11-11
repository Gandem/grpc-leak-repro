FROM python:3.9-bullseye
WORKDIR /code
EXPOSE 5000
COPY requirements.txt .
RUN pip install -rrequirements.txt
COPY . .
