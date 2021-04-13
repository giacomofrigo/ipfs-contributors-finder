# ipfs-contributors-finder
Simple IPFS contributors finder. Peer 2 Peer system and Blockchain midterm exam @ UNIPI.
 
This simple project could be used to track and show interesting statistics about the peers that contributes to the download of a 
specific file in the IPFS network.

Since there are many tools available that allow to download files from the IPFS network,
this application will not provide to the user the downloaded file. In fact, every time a donwload
is completed the cache is cleared and the downloaded file is removed.

## Stats
This application can be used to track which are the peers that contributes to download the file,
in particular it reports their *peer identifier*, thier *ip address* and the *total amount of blocks downloaded from that peer*.
A nice stat about the *countries* from which each peer share their content is also displayed.


## Installation
Download the code from this reposotory and then build the docker image by the following command
```
docker build -t ipfs-contributors-finder .
```
Finally run the application using:
```
docker run --name ipfs-contributors-finder -p 4444:4444 ipfs-contributors-finder
```
The application will be then available at *http://127.0.0.1:4444*

## Implementation
This application is a web application. It is implemented using Python Flask microframework
as backend and a simple Bootstrap based single HTML page as frontend.
Under the hood the Go implementation of IPFS is used. IPFS provides a nice Command Line Interface
The user interface uses JavaScript in order to be responsive and interact with Flask backend.
The user interface uses HighCharts (https://www.highcharts.com/) and DataTables (https://datatables.net/) libraries to create awesome interfaces. 
