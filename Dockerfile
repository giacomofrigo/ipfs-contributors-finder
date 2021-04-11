FROM alpine:latest
ENV LC_ALL=C.UTF8
ENV LANG=C.UTF8

#install go-ipfs
RUN apk add go-ipfs
#install python and pip
RUN apk add python3 py3-pip py3-setuptools

#create /app
RUN mkdir /app

#copy files
COPY app.py /app
COPY requirements.txt /app
COPY ipfs /app

WORKDIR /app

#install app reqs
RUN pip3 install -r requirements.txt

EXPOSE 4444
CMD ["python3", "app.py"]




