FROM python:3.6

ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD ./movieApis /usr/src/app/movieApis
ADD ./netguruRestApi /usr/src/app/netguruRestApi
ADD ./db.sqlite3 /usr/src/app/
ADD ./manage.py /usr/src/app/

RUN ls

RUN cd /usr/src/app/
RUN ls
EXPOSE 3000

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
