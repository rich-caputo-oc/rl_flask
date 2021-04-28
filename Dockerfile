FROM python:3.7-slim-buster

# Download latest listing of available packages:
RUN apt-get -y update && \
    apt-get -y upgrade

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt
EXPOSE 4000

# Run Flask App
CMD ["python", "rl_flask/app.py"]
