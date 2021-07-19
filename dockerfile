
FROM python:3.8.6-alpine

WORKDIR /app
COPY . /app

# COPY requirements.txt /app/

RUN apk add postgresql-dev ffmpeg libressl-dev libffi-dev gcc musl-dev gcc g++ python3-dev musl-dev zlib-dev jpeg-dev #--(5.2)

# RUN pip install --upgrade pip
# RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install --upgrade pip
# COPY . ./

RUN pip install -r requirements.txt

# RUN pip install —upgrade pip

COPY . /app
# flask를 구동하는데 필요한 패키지들을 다운로드합니다.
# local에서 실행한 후, 
# pip freeze > requirements.txt
# 를 실행하면 local에서 실행중인 flask가 필요로 했던 packages 목록을 볼 수 있음.

# RUN pip install dnspython flask-pymongo python-dotenv

# RUN flask run

# CMD ["flask", "run"]
# docker stop $(docker ps -aq)
# docker system prune -a