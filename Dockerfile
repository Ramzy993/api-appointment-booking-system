
FROM python:3.8
WORKDIR /app
RUN apt-get update
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
COPY . /app
EXPOSE 8008
CMD ["python3", "./launch_app.py"]