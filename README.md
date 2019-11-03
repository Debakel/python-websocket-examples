# Python Websockets Example
Examples of using [Tornado](https://github.com/tornadoweb/tornado) to handle websocket connections.

## Requirements
* Python 3.6
* Tornado

## Installation

    pip install -r requirements.txt
  
## Run server

    python app.py
    
## Connect
Use a websocket client (e.g. [this browser extension](https://chrome.google.com/webstore/detail/simple-websocket-client/pfdhoblngboilpfeibdedpjgfnlcodoo)  ) to connect and play around with the server. The following ressources are available:

* `ws://localhost:8001/echo` - Echoes back incoming messages.
* `ws://localhost:8001/chat` - Distributes incoming messages to all other connected clients.
* `ws://localhost:8001/time` - Sends the current datetime every 3 seconds
