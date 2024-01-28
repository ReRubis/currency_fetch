# web_cur
A dummy web app made as a test-task for a job interview.

Makes use of the following technologies:
-WebSockets,
-FastAPI,
-multiprocessing,
-Docker,

Uses separate proceses for handling the WebSocket connections and the FastAPI server.
multiprocessing.Queue is used for communication between the processes.

The WebSocket process is responsible for handling the WebSocket connections and sending the messages to OKX. 
The FastAPI process is responsible for handling the users requests. 


## How to run
Clone the repository.

Enter the project directory.
```sh
cd web_cur
```

Run the following command:
```sh
sudo docker-compose -f .prodcontainer/docker-compose.yaml build --no-cache
```

After the build is complete, run the following command:
```sh
sudo docker-compose -f .prodcontainer/docker-compose.yaml up
```
