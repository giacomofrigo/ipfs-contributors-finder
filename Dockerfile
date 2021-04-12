FROM alpine:latest
ENV LC_ALL=C.UTF8
ENV LANG=C.UTF8

LABEL maintainer="g.frigo@studenti.unipi.it"

#install go-ipfs
RUN apk add go-ipfs
#init ipfs
RUN ipfs init

#install python and pip
RUN apk add python3 py3-pip py3-setuptools

#create /app
RUN mkdir /app

#copy files
COPY . /app

#move to /app directory
WORKDIR /app

#install app reqs
RUN pip3 install -r requirements.txt

EXPOSE 4444/tcp
EXPOSE 5001/tcp

#start app
ENTRYPOINT ["python3"]
CMD ["app.py"]




