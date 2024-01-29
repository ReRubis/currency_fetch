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

## Endpoints
- /api/exchange/courses
- /api/exchange/?pair_name= 
pair_name is required and can be one of the following: BTC-USDT, ETH-USDT, XRP-USDT

## How to run
Clone the repository.

Enter the project directory.
```sh
cd web_cur
```

Create a config.yaml file
```sh
nano config.yaml
```

Config.yaml
```yaml
OKX_API_KEY: 
OKX_SECRET: 
OKX_BASE_PUBLIC_URL: wss://ws.okx.com:8443/ws/v5/public


CURRENCY_PAIRS: ['BTC-USDT', 'ETH-USDT', 'XRP-USDT']
```

Run the following command:
```sh
sudo docker-compose -f .prodcontainer/docker-compose.yaml build --no-cache
```

After the build is complete, run the following command:
```sh
sudo docker-compose -f .prodcontainer/docker-compose.yaml up
```
