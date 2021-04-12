# ipfs-contributors-finder
Simple IPFS contributors finder. Peer 2 Peer system and Blockchain midterm exam @ UNIPI.
 
This simple project could be used to track and show interesting statistics about the peers that contributes to the download of a 
specific file in the IPFS network.

Since there are many tools available that allow to download files from the IPFS network,
this application will not provide to the user the downloaded file. In fact, every time a donwload
is completed the cache is clear and the downloaded file is removed.

## Stats
This application can be used to track which are the peers that contributes ro download the file,
in particular it report their *peer identifier*, *ip address*, *total amount of blocks downloaded from that peer*.
A nice graph about the *country* from which peer share their content is also displayed.


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
