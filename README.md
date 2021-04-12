# ipfs-contributors-finder
Simple IPFS contributors finder. Peer 2 Peer system and Blockchain midterm exam @ UNIPI 
## Installation
Download the code from this reposotory and then build the docker image by the following command
```
docker build -t ipfs-contributors-finder .
```
Finally run the application using:
```
docke run --name ipfs-contributors-finder -p 4444:4444 ipfs-contributors-finder
```
The application will be then available at *http://127.0.0.1:4444*
